from functools import cached_property
from typing import IO, Dict, List, Optional, Type, cast

from ansiscape import bright_blue, bright_yellow
from ansiscape.checks import should_emit_codes

from cfp.exceptions import NoResolverError
from cfp.resolver_factories import (
    AnyResolverFactory,
    ParameterStoreResolverFactory,
    StringResolverFactory,
    UsePreviousValueResolverFactory,
)
from cfp.resolvers import AnyResolver
from cfp.sources import AnySource
from cfp.types import ApiParameter, StackParameterKey

Factories = Dict[Type[AnyResolverFactory], Optional[AnyResolverFactory]]


class StackParameters:
    """
    A list of CloudFormation stack parameters.

    Check if a parameter has been added via ``in``:

    .. code-block:: python

       >>> "foo" in stack_parameters

    Get a parameter's source by querying the key:

    .. code-block:: python

       >>> stack_parameters["foo"]

    Count the added parameters via ``len``:

    .. code-block:: python

       >>> len(stack_parameters)

    Arguments:
        default_resolvers: Register the default resolvers
    """

    def __init__(self, default_resolvers: bool = True) -> None:
        self._factories: Factories = {}
        """Factory types and lazy-loaded instances."""

        self._resolvers: List[AnyResolver] = []
        """Resolvers instantiated for this session."""

        if default_resolvers:
            self.register_resolver(StringResolverFactory)
            self.register_resolver(ParameterStoreResolverFactory)
            self.register_resolver(UsePreviousValueResolverFactory)

    def __contains__(self, key: str) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __getitem__(self, key: str) -> AnySource:
        for resolver in self._resolvers:
            if key in resolver:
                return cast(AnySource, resolver[key])
        raise KeyError(key)

    def __len__(self) -> int:
        return sum([len(resolver) for resolver in self._resolvers])

    def _find_factory(self, source: AnySource) -> Type[AnyResolverFactory]:
        for factory_type in self._factories:
            if factory_type.can_resolve(source):
                return factory_type
        raise NoResolverError(source)

    def _get_factory(self, t: Type[AnyResolverFactory]) -> AnyResolverFactory:
        if existing := self._factories.get(t, None):
            return existing

        f = t()
        self._factories[t] = f
        return f

    def add(self, key: StackParameterKey, source: AnySource) -> None:
        """
        Adds a new stack parameter with direction for finding the value.

        Arguments:
            key: Stack parameter key
            source: Value or source
        """

        factory_type = self._find_factory(source)
        factory = self._get_factory(factory_type)
        resolver = factory.try_make(source)
        resolver.queue(key=key, source=source)
        if resolver not in self._resolvers:
            self._resolvers.append(resolver)

    @cached_property
    def api_parameters(self) -> List[ApiParameter]:
        """
        Gets the resolved parameters as a list ready to pass directly to Boto3.
        """

        cf_params: List[ApiParameter] = []

        for resolver in self._resolvers:
            for cf_param in resolver.resolve():
                cf_params.append(cf_param)

        return cf_params

    def register_resolver(self, factory: Type[AnyResolverFactory]) -> None:
        """
        Registers a resolver factory.

        Arguments:
            factory: Factory type
        """

        self._factories[factory] = None

    def render(self, writer: IO[str], color: Optional[bool] = None) -> None:
        """
        Renders the parameters.

        Arguments:
            writer: String writer.
            color: Emit color. The default `None` delegates the decision to Ansiscape.
        """

        longest = max([len(p.get("ParameterKey", "")) for p in self.api_parameters])

        for p in self.api_parameters:
            key = p.get("ParameterKey", "")

            if p.get("UsePreviousValue", False):
                value = "<previous value>"
            else:
                value = p.get("ParameterValue", "")

            padding = " " * (longest - len(key))

            if color is None:
                color = should_emit_codes()

            if color:
                key = bright_blue(key).encoded
                value = bright_yellow(value).encoded

            writer.write(f"{key}{padding} = {value}\n")
