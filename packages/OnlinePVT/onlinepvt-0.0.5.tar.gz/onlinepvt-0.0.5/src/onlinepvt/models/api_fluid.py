import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.api_fluid_kij import ApiFluidKij
from ..models.api_fluid_polymer_component import ApiFluidPolymerComponent
from ..models.api_fluid_standard_component import ApiFluidStandardComponent
from ..models.cp_model import CpModel
from ..models.eos_model import EosModel
from ..models.property_reference_point import PropertyReferencePoint
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiFluid")


@attr.s(auto_attribs=True)
class ApiFluid:
    """Information for a fluid"""

    fluid_id: Union[Unset, str] = UNSET
    creation_time: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    comment: Union[Unset, None, str] = UNSET
    eos: Union[Unset, EosModel] = UNSET
    property_reference_point: Union[Unset, PropertyReferencePoint] = UNSET
    solvent_cp: Union[Unset, CpModel] = UNSET
    polymer_cp: Union[Unset, CpModel] = UNSET
    standards: Union[Unset, None, List[ApiFluidStandardComponent]] = UNSET
    polymers: Union[Unset, None, List[ApiFluidPolymerComponent]] = UNSET
    kij: Union[Unset, None, List[ApiFluidKij]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fluid_id = self.fluid_id
        creation_time: Union[Unset, str] = UNSET
        if not isinstance(self.creation_time, Unset):
            creation_time = self.creation_time.isoformat()

        name = self.name
        comment = self.comment
        eos: Union[Unset, str] = UNSET
        if not isinstance(self.eos, Unset):
            eos = self.eos.value

        property_reference_point: Union[Unset, str] = UNSET
        if not isinstance(self.property_reference_point, Unset):
            property_reference_point = self.property_reference_point.value

        solvent_cp: Union[Unset, str] = UNSET
        if not isinstance(self.solvent_cp, Unset):
            solvent_cp = self.solvent_cp.value

        polymer_cp: Union[Unset, str] = UNSET
        if not isinstance(self.polymer_cp, Unset):
            polymer_cp = self.polymer_cp.value

        standards: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.standards, Unset):
            if self.standards is None:
                standards = None
            else:
                standards = []
                for standards_item_data in self.standards:
                    standards_item = standards_item_data.to_dict()

                    standards.append(standards_item)

        polymers: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.polymers, Unset):
            if self.polymers is None:
                polymers = None
            else:
                polymers = []
                for polymers_item_data in self.polymers:
                    polymers_item = polymers_item_data.to_dict()

                    polymers.append(polymers_item)

        kij: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.kij, Unset):
            if self.kij is None:
                kij = None
            else:
                kij = []
                for kij_item_data in self.kij:
                    kij_item = kij_item_data.to_dict()

                    kij.append(kij_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fluid_id is not UNSET:
            field_dict["fluidId"] = fluid_id
        if creation_time is not UNSET:
            field_dict["creationTime"] = creation_time
        if name is not UNSET:
            field_dict["name"] = name
        if comment is not UNSET:
            field_dict["comment"] = comment
        if eos is not UNSET:
            field_dict["eos"] = eos
        if property_reference_point is not UNSET:
            field_dict["propertyReferencePoint"] = property_reference_point
        if solvent_cp is not UNSET:
            field_dict["solventCp"] = solvent_cp
        if polymer_cp is not UNSET:
            field_dict["polymerCp"] = polymer_cp
        if standards is not UNSET:
            field_dict["standards"] = standards
        if polymers is not UNSET:
            field_dict["polymers"] = polymers
        if kij is not UNSET:
            field_dict["kij"] = kij

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fluid_id = d.pop("fluidId", UNSET)

        _creation_time = d.pop("creationTime", UNSET)
        creation_time: Union[Unset, datetime.datetime]
        if isinstance(_creation_time, Unset):
            creation_time = UNSET
        else:
            creation_time = isoparse(_creation_time)

        name = d.pop("name", UNSET)

        comment = d.pop("comment", UNSET)

        _eos = d.pop("eos", UNSET)
        eos: Union[Unset, EosModel]
        if isinstance(_eos, Unset):
            eos = UNSET
        else:
            eos = EosModel(_eos)

        _property_reference_point = d.pop("propertyReferencePoint", UNSET)
        property_reference_point: Union[Unset, PropertyReferencePoint]
        if isinstance(_property_reference_point, Unset):
            property_reference_point = UNSET
        else:
            property_reference_point = PropertyReferencePoint(_property_reference_point)

        _solvent_cp = d.pop("solventCp", UNSET)
        solvent_cp: Union[Unset, CpModel]
        if isinstance(_solvent_cp, Unset):
            solvent_cp = UNSET
        else:
            solvent_cp = CpModel(_solvent_cp)

        _polymer_cp = d.pop("polymerCp", UNSET)
        polymer_cp: Union[Unset, CpModel]
        if isinstance(_polymer_cp, Unset):
            polymer_cp = UNSET
        else:
            polymer_cp = CpModel(_polymer_cp)

        standards = []
        _standards = d.pop("standards", UNSET)
        for standards_item_data in _standards or []:
            standards_item = ApiFluidStandardComponent.from_dict(standards_item_data)

            standards.append(standards_item)

        polymers = []
        _polymers = d.pop("polymers", UNSET)
        for polymers_item_data in _polymers or []:
            polymers_item = ApiFluidPolymerComponent.from_dict(polymers_item_data)

            polymers.append(polymers_item)

        kij = []
        _kij = d.pop("kij", UNSET)
        for kij_item_data in _kij or []:
            kij_item = ApiFluidKij.from_dict(kij_item_data)

            kij.append(kij_item)

        api_fluid = cls(
            fluid_id=fluid_id,
            creation_time=creation_time,
            name=name,
            comment=comment,
            eos=eos,
            property_reference_point=property_reference_point,
            solvent_cp=solvent_cp,
            polymer_cp=polymer_cp,
            standards=standards,
            polymers=polymers,
            kij=kij,
        )

        return api_fluid
