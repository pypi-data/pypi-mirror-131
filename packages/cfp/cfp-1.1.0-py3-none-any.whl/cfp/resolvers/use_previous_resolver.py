from typing import Iterator

from cfp.resolvers.resolver import Resolver
from cfp.sources import UsePreviousValue
from cfp.types import ApiParameter


class UsePreviousValueResolver(Resolver[UsePreviousValue]):
    def resolve(self) -> Iterator[ApiParameter]:
        """
        Invokes the queued resolution tasks and returns an iterator of the
        values.
        """

        for key in self._sources:
            yield ApiParameter(ParameterKey=key, UsePreviousValue=True)
