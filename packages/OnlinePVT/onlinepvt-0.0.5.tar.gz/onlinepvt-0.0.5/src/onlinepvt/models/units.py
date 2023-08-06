from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.units_item import UnitsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Units")


@attr.s(auto_attribs=True)
class Units:
    """Holds all unit information"""

    temperature: Union[Unset, UnitsItem] = UNSET
    pressure: Union[Unset, UnitsItem] = UNSET
    composition: Union[Unset, UnitsItem] = UNSET
    enthalpy: Union[Unset, UnitsItem] = UNSET
    entropy: Union[Unset, UnitsItem] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        temperature: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.temperature, Unset):
            temperature = self.temperature.to_dict()

        pressure: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pressure, Unset):
            pressure = self.pressure.to_dict()

        composition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.composition, Unset):
            composition = self.composition.to_dict()

        enthalpy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.enthalpy, Unset):
            enthalpy = self.enthalpy.to_dict()

        entropy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entropy, Unset):
            entropy = self.entropy.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure
        if composition is not UNSET:
            field_dict["composition"] = composition
        if enthalpy is not UNSET:
            field_dict["enthalpy"] = enthalpy
        if entropy is not UNSET:
            field_dict["entropy"] = entropy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _temperature = d.pop("temperature", UNSET)
        temperature: Union[Unset, UnitsItem]
        if isinstance(_temperature, Unset):
            temperature = UNSET
        else:
            temperature = UnitsItem.from_dict(_temperature)

        _pressure = d.pop("pressure", UNSET)
        pressure: Union[Unset, UnitsItem]
        if isinstance(_pressure, Unset):
            pressure = UNSET
        else:
            pressure = UnitsItem.from_dict(_pressure)

        _composition = d.pop("composition", UNSET)
        composition: Union[Unset, UnitsItem]
        if isinstance(_composition, Unset):
            composition = UNSET
        else:
            composition = UnitsItem.from_dict(_composition)

        _enthalpy = d.pop("enthalpy", UNSET)
        enthalpy: Union[Unset, UnitsItem]
        if isinstance(_enthalpy, Unset):
            enthalpy = UNSET
        else:
            enthalpy = UnitsItem.from_dict(_enthalpy)

        _entropy = d.pop("entropy", UNSET)
        entropy: Union[Unset, UnitsItem]
        if isinstance(_entropy, Unset):
            entropy = UNSET
        else:
            entropy = UnitsItem.from_dict(_entropy)

        units = cls(
            temperature=temperature,
            pressure=pressure,
            composition=composition,
            enthalpy=enthalpy,
            entropy=entropy,
        )

        return units
