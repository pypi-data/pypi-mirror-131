from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.access_policy import AccessPolicy
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccessPoliciesPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class AccessPoliciesPaginatedList:
    """  """

    _access_policies: Union[Unset, List[AccessPolicy]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("access_policies={}".format(repr(self._access_policies)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "AccessPoliciesPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        access_policies: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._access_policies, Unset):
            access_policies = []
            for access_policies_item_data in self._access_policies:
                access_policies_item = access_policies_item_data.to_dict()

                access_policies.append(access_policies_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if access_policies is not UNSET:
            field_dict["accessPolicies"] = access_policies
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access_policies = []
        _access_policies = d.pop("accessPolicies", UNSET)
        for access_policies_item_data in _access_policies or []:
            access_policies_item = AccessPolicy.from_dict(access_policies_item_data)

            access_policies.append(access_policies_item)

        next_token = d.pop("nextToken", UNSET)

        access_policies_paginated_list = cls(
            access_policies=access_policies,
            next_token=next_token,
        )

        return access_policies_paginated_list

    @property
    def access_policies(self) -> List[AccessPolicy]:
        if isinstance(self._access_policies, Unset):
            raise NotPresentError(self, "access_policies")
        return self._access_policies

    @access_policies.setter
    def access_policies(self, value: List[AccessPolicy]) -> None:
        self._access_policies = value

    @access_policies.deleter
    def access_policies(self) -> None:
        self._access_policies = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
