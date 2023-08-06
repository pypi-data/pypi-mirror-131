from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnitsItem")


@attr.s(auto_attribs=True)
class UnitsItem:
    """In and out units"""

    in_: Union[Unset, None, str] = UNSET
    out: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        in_ = self.in_
        out = self.out

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if in_ is not UNSET:
            field_dict["in"] = in_
        if out is not UNSET:
            field_dict["out"] = out

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        in_ = d.pop("in", UNSET)

        out = d.pop("out", UNSET)

        units_item = cls(
            in_=in_,
            out=out,
        )

        return units_item
