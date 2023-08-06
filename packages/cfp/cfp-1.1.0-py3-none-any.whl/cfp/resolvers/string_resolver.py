from typing import Iterator

from cfp.resolvers.resolver import Resolver
from cfp.types import ApiParameter


class StringResolver(Resolver[str]):
    def resolve(self) -> Iterator[ApiParameter]:
        for k in self._sources:
            yield ApiParameter(ParameterKey=k, ParameterValue=self._sources[k])
