from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calculation_composition import CalculationComposition
from ..models.units import Units
from ..types import UNSET, Unset

T = TypeVar("T", bound="PhasediagramFixedTemperaturePressureCalculationInput")


@attr.s(auto_attribs=True)
class PhasediagramFixedTemperaturePressureCalculationInput:
    """Input to phase diagram calculation at fixed temperature/pressure"""

    user_id: str
    access_secret: str
    components: List[CalculationComposition]
    fluid_id: str
    units: Union[Unset, Units] = UNSET
    vlle: Union[Unset, bool] = UNSET
    sle: Union[Unset, bool] = UNSET
    slve: Union[Unset, bool] = UNSET
    spinodal: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        access_secret = self.access_secret
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()

            components.append(components_item)

        fluid_id = self.fluid_id
        units: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.units, Unset):
            units = self.units.to_dict()

        vlle = self.vlle
        sle = self.sle
        slve = self.slve
        spinodal = self.spinodal

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
                "accessSecret": access_secret,
                "components": components,
                "fluidId": fluid_id,
            }
        )
        if units is not UNSET:
            field_dict["units"] = units
        if vlle is not UNSET:
            field_dict["vlle"] = vlle
        if sle is not UNSET:
            field_dict["sle"] = sle
        if slve is not UNSET:
            field_dict["slve"] = slve
        if spinodal is not UNSET:
            field_dict["spinodal"] = spinodal

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userId")

        access_secret = d.pop("accessSecret")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = CalculationComposition.from_dict(components_item_data)

            components.append(components_item)

        fluid_id = d.pop("fluidId")

        _units = d.pop("units", UNSET)
        units: Union[Unset, Units]
        if isinstance(_units, Unset):
            units = UNSET
        else:
            units = Units.from_dict(_units)

        vlle = d.pop("vlle", UNSET)

        sle = d.pop("sle", UNSET)

        slve = d.pop("slve", UNSET)

        spinodal = d.pop("spinodal", UNSET)

        phasediagram_fixed_temperature_pressure_calculation_input = cls(
            user_id=user_id,
            access_secret=access_secret,
            components=components,
            fluid_id=fluid_id,
            units=units,
            vlle=vlle,
            sle=sle,
            slve=slve,
            spinodal=spinodal,
        )

        return phasediagram_fixed_temperature_pressure_calculation_input
