# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetZonesResult',
    'AwaitableGetZonesResult',
    'get_zones',
]

@pulumi.output_type
class GetZonesResult:
    """
    A collection of values returned by getZones.
    """
    def __init__(__self__, default_zone=None, id=None, zones=None):
        if default_zone and not isinstance(default_zone, str):
            raise TypeError("Expected argument 'default_zone' to be a str")
        pulumi.set(__self__, "default_zone", default_zone)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="defaultZone")
    def default_zone(self) -> str:
        return pulumi.get(self, "default_zone")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        return pulumi.get(self, "zones")


class AwaitableGetZonesResult(GetZonesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetZonesResult(
            default_zone=self.default_zone,
            id=self.id,
            zones=self.zones)


def get_zones(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetZonesResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('databricks:databricks/getZones:getZones', __args__, opts=opts, typ=GetZonesResult).value

    return AwaitableGetZonesResult(
        default_zone=__ret__.default_zone,
        id=__ret__.id,
        zones=__ret__.zones)
