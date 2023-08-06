from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.activation_metadata_request_model import ActivationMetadataRequestModel
from ..models.activation_meter_attribute_request_model import ActivationMeterAttributeRequestModel
from ..models.activation_request_model_os import ActivationRequestModelOs
from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationRequestModel")


@attr.s(auto_attribs=True)
class ActivationRequestModel:
    """ """

    os: ActivationRequestModelOs
    fingerprint: str
    hostname: str
    app_version: str
    user_hash: str
    product_id: str
    key: str
    os_version: Union[Unset, None, str] = UNSET
    vm_name: Union[Unset, None, str] = UNSET
    container: Union[Unset, None, bool] = UNSET
    email: Union[Unset, None, str] = UNSET
    password: Union[Unset, None, str] = UNSET
    lease_duration: Union[Unset, None, int] = UNSET
    metadata: Union[Unset, None, List[ActivationMetadataRequestModel]] = UNSET
    meter_attributes: Union[Unset, None, List[ActivationMeterAttributeRequestModel]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        os = self.os.value

        fingerprint = self.fingerprint
        hostname = self.hostname
        app_version = self.app_version
        user_hash = self.user_hash
        product_id = self.product_id
        key = self.key
        os_version = self.os_version
        vm_name = self.vm_name
        container = self.container
        email = self.email
        password = self.password
        lease_duration = self.lease_duration
        metadata: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            if self.metadata is None:
                metadata = None
            else:
                metadata = []
                for metadata_item_data in self.metadata:
                    metadata_item = metadata_item_data.to_dict()

                    metadata.append(metadata_item)

        meter_attributes: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.meter_attributes, Unset):
            if self.meter_attributes is None:
                meter_attributes = None
            else:
                meter_attributes = []
                for meter_attributes_item_data in self.meter_attributes:
                    meter_attributes_item = meter_attributes_item_data.to_dict()

                    meter_attributes.append(meter_attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "os": os,
                "fingerprint": fingerprint,
                "hostname": hostname,
                "appVersion": app_version,
                "userHash": user_hash,
                "productId": product_id,
                "key": key,
            }
        )
        if os_version is not UNSET:
            field_dict["osVersion"] = os_version
        if vm_name is not UNSET:
            field_dict["vmName"] = vm_name
        if container is not UNSET:
            field_dict["container"] = container
        if email is not UNSET:
            field_dict["email"] = email
        if password is not UNSET:
            field_dict["password"] = password
        if lease_duration is not UNSET:
            field_dict["leaseDuration"] = lease_duration
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if meter_attributes is not UNSET:
            field_dict["meterAttributes"] = meter_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        os = ActivationRequestModelOs(d.pop("os"))

        fingerprint = d.pop("fingerprint")

        hostname = d.pop("hostname")

        app_version = d.pop("appVersion")

        user_hash = d.pop("userHash")

        product_id = d.pop("productId")

        key = d.pop("key")

        os_version = d.pop("osVersion", UNSET)

        vm_name = d.pop("vmName", UNSET)

        container = d.pop("container", UNSET)

        email = d.pop("email", UNSET)

        password = d.pop("password", UNSET)

        lease_duration = d.pop("leaseDuration", UNSET)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = ActivationMetadataRequestModel.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        meter_attributes = []
        _meter_attributes = d.pop("meterAttributes", UNSET)
        for meter_attributes_item_data in _meter_attributes or []:
            meter_attributes_item = ActivationMeterAttributeRequestModel.from_dict(meter_attributes_item_data)

            meter_attributes.append(meter_attributes_item)

        activation_request_model = cls(
            os=os,
            fingerprint=fingerprint,
            hostname=hostname,
            app_version=app_version,
            user_hash=user_hash,
            product_id=product_id,
            key=key,
            os_version=os_version,
            vm_name=vm_name,
            container=container,
            email=email,
            password=password,
            lease_duration=lease_duration,
            metadata=metadata,
            meter_attributes=meter_attributes,
        )

        return activation_request_model
