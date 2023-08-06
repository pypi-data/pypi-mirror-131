from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calculation_composition import CalculationComposition
from ..models.cloud_point_calculation_type import CloudPointCalculationType
from ..models.units import Units
from ..types import UNSET, Unset

T = TypeVar("T", bound="CloudPointCalculationInput")


@attr.s(auto_attribs=True)
class CloudPointCalculationInput:
    """Input to cloud point calculation"""

    user_id: str
    access_secret: str
    components: List[CalculationComposition]
    fluid_id: str
    point_type: CloudPointCalculationType
    units: Union[Unset, Units] = UNSET
    temperature: Union[Unset, float] = UNSET
    pressure: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        access_secret = self.access_secret
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()

            components.append(components_item)

        fluid_id = self.fluid_id
        point_type = self.point_type.value

        units: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.units, Unset):
            units = self.units.to_dict()

        temperature = self.temperature
        pressure = self.pressure

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
                "accessSecret": access_secret,
                "components": components,
                "fluidId": fluid_id,
                "pointType": point_type,
            }
        )
        if units is not UNSET:
            field_dict["units"] = units
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure

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

        point_type = CloudPointCalculationType(d.pop("pointType"))

        _units = d.pop("units", UNSET)
        units: Union[Unset, Units]
        if isinstance(_units, Unset):
            units = UNSET
        else:
            units = Units.from_dict(_units)

        temperature = d.pop("temperature", UNSET)

        pressure = d.pop("pressure", UNSET)

        cloud_point_calculation_input = cls(
            user_id=user_id,
            access_secret=access_secret,
            components=components,
            fluid_id=fluid_id,
            point_type=point_type,
            units=units,
            temperature=temperature,
            pressure=pressure,
        )

        return cloud_point_calculation_input
