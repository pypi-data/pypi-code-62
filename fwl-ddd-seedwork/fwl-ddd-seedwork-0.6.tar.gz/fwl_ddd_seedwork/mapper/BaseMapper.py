import abc

from fwl_ddd_seedwork import DTO, Entity
from fwl_ddd_seedwork.infrastructure import Schema


class BaseMapper(abc.ABC):

    @abc.abstractmethod
    def dto_to_domain(self, dto: DTO) -> Entity:
        raise NotImplementedError

    @abc.abstractmethod
    def domain_to_dto(self, entity: Entity) -> DTO:
        raise NotImplementedError

    @abc.abstractmethod
    def domain_to_schema(self, entity: Entity) -> Schema:
        raise NotImplementedError

    @abc.abstractmethod
    def schema_to_domain(self, schema: Schema) -> Entity:
        raise NotImplementedError
