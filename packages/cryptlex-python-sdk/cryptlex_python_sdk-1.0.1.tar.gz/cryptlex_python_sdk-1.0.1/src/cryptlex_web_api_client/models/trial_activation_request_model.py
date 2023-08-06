from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.trial_activation_metadata_request_model import TrialActivationMetadataRequestModel
from ..models.trial_activation_request_model_os import TrialActivationRequestModelOs
from ..types import UNSET, Unset

T = TypeVar("T", bound="TrialActivationRequestModel")


@attr.s(auto_attribs=True)
class TrialActivationRequestModel:
    """ """

    os: Union[Unset, TrialActivationRequestModelOs] = UNSET
    os_version: Union[Unset, None, str] = UNSET
    fingerprint: Union[Unset, str] = UNSET
    vm_name: Union[Unset, None, str] = UNSET
    container: Union[Unset, None, bool] = UNSET
    hostname: Union[Unset, str] = UNSET
    app_version: Union[Unset, str] = UNSET
    user_hash: Union[Unset, str] = UNSET
    product_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, None, List[TrialActivationMetadataRequestModel]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        os: Union[Unset, str] = UNSET
        if not isinstance(self.os, Unset):
            os = self.os.value

        os_version = self.os_version
        fingerprint = self.fingerprint
        vm_name = self.vm_name
        container = self.container
        hostname = self.hostname
        app_version = self.app_version
        user_hash = self.user_hash
        product_id = self.product_id
        metadata: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            if self.metadata is None:
                metadata = None
            else:
                metadata = []
                for metadata_item_data in self.metadata:
                    metadata_item = metadata_item_data.to_dict()

                    metadata.append(metadata_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if os is not UNSET:
            field_dict["os"] = os
        if os_version is not UNSET:
            field_dict["osVersion"] = os_version
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint
        if vm_name is not UNSET:
            field_dict["vmName"] = vm_name
        if container is not UNSET:
            field_dict["container"] = container
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if app_version is not UNSET:
            field_dict["appVersion"] = app_version
        if user_hash is not UNSET:
            field_dict["userHash"] = user_hash
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _os = d.pop("os", UNSET)
        os: Union[Unset, TrialActivationRequestModelOs]
        if isinstance(_os, Unset):
            os = UNSET
        else:
            os = TrialActivationRequestModelOs(_os)

        os_version = d.pop("osVersion", UNSET)

        fingerprint = d.pop("fingerprint", UNSET)

        vm_name = d.pop("vmName", UNSET)

        container = d.pop("container", UNSET)

        hostname = d.pop("hostname", UNSET)

        app_version = d.pop("appVersion", UNSET)

        user_hash = d.pop("userHash", UNSET)

        product_id = d.pop("productId", UNSET)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = TrialActivationMetadataRequestModel.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        trial_activation_request_model = cls(
            os=os,
            os_version=os_version,
            fingerprint=fingerprint,
            vm_name=vm_name,
            container=container,
            hostname=hostname,
            app_version=app_version,
            user_hash=user_hash,
            product_id=product_id,
            metadata=metadata,
        )

        return trial_activation_request_model
