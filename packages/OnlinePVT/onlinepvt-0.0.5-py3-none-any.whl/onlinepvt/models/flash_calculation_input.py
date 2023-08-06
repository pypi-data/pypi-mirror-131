from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calculation_composition import CalculationComposition
from ..models.flash_calculation_type import FlashCalculationType
from ..models.units import Units
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlashCalculationInput")


@attr.s(auto_attribs=True)
class FlashCalculationInput:
    """Input for flash calculation"""

    user_id: str
    access_secret: str
    components: List[CalculationComposition]
    flash_type: FlashCalculationType
    fluid_id: str
    units: Union[Unset, Units] = UNSET
    temperature: Union[Unset, float] = UNSET
    pressure: Union[Unset, float] = UNSET
    enthalpy: Union[Unset, float] = UNSET
    entropy: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        access_secret = self.access_secret
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()

            components.append(components_item)

        flash_type = self.flash_type.value

        units: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.units, Unset):
            units = self.units.to_dict()

        fluid_id = self.fluid_id
        temperature = self.temperature
        pressure = self.pressure
        enthalpy = self.enthalpy
        entropy = self.entropy

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
                "accessSecret": access_secret,
                "components": components,
                "flashType": flash_type,
            }
        )
        if units is not UNSET:
            field_dict["units"] = units
        if fluid_id is not UNSET:
            field_dict["fluidId"] = fluid_id
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure
        if enthalpy is not UNSET:
            field_dict["enthalpy"] = enthalpy
        if entropy is not UNSET:
            field_dict["entropy"] = entropy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userId")

        access_secret = d.pop("accessSecret")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = CalculationComposition.from_dict(
                components_item_data)

            components.append(components_item)

        flash_type = FlashCalculationType(d.pop("flashType"))

        _units = d.pop("units", UNSET)
        units: Union[Unset, Units]
        if isinstance(_units, Unset):
            units = UNSET
        else:
            units = Units.from_dict(_units)

        fluid_id = d.pop("fluidId", UNSET)

        temperature = d.pop("temperature", UNSET)

        pressure = d.pop("pressure", UNSET)

        enthalpy = d.pop("enthalpy", UNSET)

        entropy = d.pop("entropy", UNSET)

        flash_calculation_input = cls(
            user_id=user_id,
            access_secret=access_secret,
            components=components,
            flash_type=flash_type,
            units=units,
            fluid_id=fluid_id,
            temperature=temperature,
            pressure=pressure,
            enthalpy=enthalpy,
            entropy=entropy,
        )

        return flash_calculation_input
