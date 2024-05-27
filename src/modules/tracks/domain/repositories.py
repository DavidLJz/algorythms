import abc
from typing import Generic, TypeVar, List
from .entities import AggregateRoot

Entity = TypeVar("Entity", bound=AggregateRoot)


class GenericRepository(Generic[Entity], metaclass=abc.ABCMeta):
    """An interface for a generic repository"""

    @abc.abstractmethod
    def find(self) -> List[Entity]:
        raise NotImplementedError()

    @abc.abstractmethod
    def insert(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity: Entity):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def upsert(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, entity: Entity):
        raise NotImplementedError()