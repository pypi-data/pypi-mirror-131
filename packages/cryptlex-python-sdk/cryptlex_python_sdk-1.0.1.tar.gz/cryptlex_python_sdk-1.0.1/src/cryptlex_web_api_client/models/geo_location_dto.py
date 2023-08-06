from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GeoLocationDto")


@attr.s(auto_attribs=True)
class GeoLocationDto:
    """ """

    ip_address: Union[Unset, None, str] = UNSET
    country_code: Union[Unset, None, str] = UNSET
    country_name: Union[Unset, None, str] = UNSET
    region_code: Union[Unset, None, str] = UNSET
    region_name: Union[Unset, None, str] = UNSET
    city: Union[Unset, None, str] = UNSET
    zip_code: Union[Unset, None, str] = UNSET
    time_zone: Union[Unset, None, str] = UNSET
    latitude: Union[Unset, None, float] = UNSET
    longitude: Union[Unset, None, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ip_address = self.ip_address
        country_code = self.country_code
        country_name = self.country_name
        region_code = self.region_code
        region_name = self.region_name
        city = self.city
        zip_code = self.zip_code
        time_zone = self.time_zone
        latitude = self.latitude
        longitude = self.longitude

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if ip_address is not UNSET:
            field_dict["ipAddress"] = ip_address
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if country_name is not UNSET:
            field_dict["countryName"] = country_name
        if region_code is not UNSET:
            field_dict["regionCode"] = region_code
        if region_name is not UNSET:
            field_dict["regionName"] = region_name
        if city is not UNSET:
            field_dict["city"] = city
        if zip_code is not UNSET:
            field_dict["zipCode"] = zip_code
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ip_address = d.pop("ipAddress", UNSET)

        country_code = d.pop("countryCode", UNSET)

        country_name = d.pop("countryName", UNSET)

        region_code = d.pop("regionCode", UNSET)

        region_name = d.pop("regionName", UNSET)

        city = d.pop("city", UNSET)

        zip_code = d.pop("zipCode", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        geo_location_dto = cls(
            ip_address=ip_address,
            country_code=country_code,
            country_name=country_name,
            region_code=region_code,
            region_name=region_name,
            city=city,
            zip_code=zip_code,
            time_zone=time_zone,
            latitude=latitude,
            longitude=longitude,
        )

        return geo_location_dto
