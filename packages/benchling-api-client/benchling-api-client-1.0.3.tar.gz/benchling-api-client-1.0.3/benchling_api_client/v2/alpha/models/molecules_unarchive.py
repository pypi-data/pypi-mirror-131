from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="MoleculesUnarchive")


@attr.s(auto_attribs=True, repr=False)
class MoleculesUnarchive:
    """The request body for unarchiving Molecules."""

    _molecule_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("molecule_ids={}".format(repr(self._molecule_ids)))
        return "MoleculesUnarchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        molecule_ids = self._molecule_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "moleculeIds": molecule_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        molecule_ids = cast(List[str], d.pop("moleculeIds"))

        molecules_unarchive = cls(
            molecule_ids=molecule_ids,
        )

        return molecules_unarchive

    @property
    def molecule_ids(self) -> List[str]:
        return self._molecule_ids

    @molecule_ids.setter
    def molecule_ids(self, value: List[str]) -> None:
        self._molecule_ids = value
