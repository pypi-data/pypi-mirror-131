from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.custom_entity_upsert import CustomEntityUpsert

T = TypeVar("T", bound="CustomEntityBulkUpsertRequest")


@attr.s(auto_attribs=True, repr=False)
class CustomEntityBulkUpsertRequest:
    """  """

    _custom_entities: List[CustomEntityUpsert]

    def __repr__(self):
        fields = []
        fields.append("custom_entities={}".format(repr(self._custom_entities)))
        return "CustomEntityBulkUpsertRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        custom_entities = []
        for custom_entities_item_data in self._custom_entities:
            custom_entities_item = custom_entities_item_data.to_dict()

            custom_entities.append(custom_entities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "customEntities": custom_entities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_entities = []
        _custom_entities = d.pop("customEntities")
        for custom_entities_item_data in _custom_entities:
            custom_entities_item = CustomEntityUpsert.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        custom_entity_bulk_upsert_request = cls(
            custom_entities=custom_entities,
        )

        return custom_entity_bulk_upsert_request

    @property
    def custom_entities(self) -> List[CustomEntityUpsert]:
        return self._custom_entities

    @custom_entities.setter
    def custom_entities(self, value: List[CustomEntityUpsert]) -> None:
        self._custom_entities = value
