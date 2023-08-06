from typing import Optional

from cfp.resolver_factories.resolver_factory import ResolverFactory
from cfp.resolvers import UsePreviousValueResolver
from cfp.sources import AnySource, UsePreviousValue


class UsePreviousValueResolverFactory(
    ResolverFactory[
        UsePreviousValue,
        UsePreviousValueResolver,
    ]
):
    def __init__(self) -> None:
        self._resolver: Optional[UsePreviousValueResolver] = None

    @staticmethod
    def can_resolve(source: AnySource) -> bool:
        return isinstance(source, UsePreviousValue)

    def make(self, source: UsePreviousValue) -> UsePreviousValueResolver:
        if self._resolver is None:
            self._resolver = UsePreviousValueResolver()
        return self._resolver
