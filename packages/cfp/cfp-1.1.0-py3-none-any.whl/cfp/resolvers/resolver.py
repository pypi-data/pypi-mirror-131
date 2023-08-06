from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Iterator, TypeVar, cast

from cfp.sources.source import AnySource, TSource
from cfp.types import ApiParameter, StackParameterKey


class Resolver(ABC, Generic[TSource]):
    """Abstract base resolver."""

    def __init__(self) -> None:
        self._sources: Dict[StackParameterKey, TSource] = {}

    def __contains__(self, key: str) -> bool:
        return key in self._sources

    def __getitem__(self, key: str) -> TSource:
        return self._sources[key]

    def __len__(self) -> int:
        return len(self._sources)

    def _queue(self, key: StackParameterKey, source: TSource) -> None:
        """
        Queues a resolution task to perform later.

        Arguments:
            key:    Stack parameter key
            source: Value source
        """

        # Override to implement as needed.
        pass

    def queue(self, key: StackParameterKey, source: AnySource) -> None:
        """
        Queues a resolution task to perform later.

        Arguments:
            key:    Stack parameter key
            source: Value source
        """

        self._sources[key] = cast(TSource, source)
        self._queue(key=key, source=cast(TSource, source))

    @abstractmethod
    def resolve(self) -> Iterator[ApiParameter]:
        """
        Invokes the queued resolution tasks and returns an iterator of the
        values.
        """


AnyResolver = Resolver[Any]

TResolver = TypeVar("TResolver", bound=AnyResolver)
