from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BenchlingAppsUnarchive")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppsUnarchive:
    """  """

    _app_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("app_ids={}".format(repr(self._app_ids)))
        return "BenchlingAppsUnarchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_ids = self._app_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "appIds": app_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        app_ids = cast(List[str], d.pop("appIds"))

        benchling_apps_unarchive = cls(
            app_ids=app_ids,
        )

        return benchling_apps_unarchive

    @property
    def app_ids(self) -> List[str]:
        """ Array of app IDs """
        return self._app_ids

    @app_ids.setter
    def app_ids(self, value: List[str]) -> None:
        self._app_ids = value
