from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_call_result import ApiCallResult
from ..models.api_fluid import ApiFluid
from ..models.exception_info import ExceptionInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestFluidResult")


@attr.s(auto_attribs=True)
class RequestFluidResult:
    """Holds result for requesting information for a fluid"""

    api_status: Union[Unset, ApiCallResult] = UNSET
    fluid: Union[Unset, ApiFluid] = UNSET
    exception_info: Union[Unset, ExceptionInfo] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        api_status: Union[Unset, str] = UNSET
        if not isinstance(self.api_status, Unset):
            api_status = self.api_status.value

        fluid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fluid, Unset):
            fluid = self.fluid.to_dict()

        exception_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exception_info, Unset):
            exception_info = self.exception_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if api_status is not UNSET:
            field_dict["apiStatus"] = api_status
        if fluid is not UNSET:
            field_dict["fluid"] = fluid
        if exception_info is not UNSET:
            field_dict["exceptionInfo"] = exception_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _api_status = d.pop("apiStatus", UNSET)
        api_status: Union[Unset, ApiCallResult]
        if isinstance(_api_status, Unset):
            api_status = UNSET
        else:
            api_status = ApiCallResult(_api_status)

        _fluid = d.pop("fluid", UNSET)
        fluid: Union[Unset, ApiFluid]
        if isinstance(_fluid, Unset):
            fluid = UNSET
        else:
            fluid = ApiFluid.from_dict(_fluid)

        _exception_info = d.pop("exceptionInfo", UNSET)
        exception_info: Union[Unset, ExceptionInfo]
        if isinstance(_exception_info, Unset):
            exception_info = UNSET
        else:
            exception_info = ExceptionInfo.from_dict(_exception_info)

        request_fluid_result = cls(
            api_status=api_status,
            fluid=fluid,
            exception_info=exception_info,
        )

        return request_fluid_result
