from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="PlanUpdateRequestModel")


@attr.s(auto_attribs=True)
class PlanUpdateRequestModel:
    """ """

    plan_id: str

    def to_dict(self) -> Dict[str, Any]:
        plan_id = self.plan_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "planId": plan_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plan_id = d.pop("planId")

        plan_update_request_model = cls(
            plan_id=plan_id,
        )

        return plan_update_request_model
