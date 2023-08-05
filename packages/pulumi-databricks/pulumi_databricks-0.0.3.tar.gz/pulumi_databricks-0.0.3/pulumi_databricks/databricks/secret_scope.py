# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['SecretScopeArgs', 'SecretScope']

@pulumi.input_type
class SecretScopeArgs:
    def __init__(__self__, *,
                 backend_type: Optional[pulumi.Input[str]] = None,
                 initial_manage_principal: Optional[pulumi.Input[str]] = None,
                 keyvault_metadata: Optional[pulumi.Input['SecretScopeKeyvaultMetadataArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SecretScope resource.
        """
        if backend_type is not None:
            pulumi.set(__self__, "backend_type", backend_type)
        if initial_manage_principal is not None:
            pulumi.set(__self__, "initial_manage_principal", initial_manage_principal)
        if keyvault_metadata is not None:
            pulumi.set(__self__, "keyvault_metadata", keyvault_metadata)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="backendType")
    def backend_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "backend_type")

    @backend_type.setter
    def backend_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend_type", value)

    @property
    @pulumi.getter(name="initialManagePrincipal")
    def initial_manage_principal(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "initial_manage_principal")

    @initial_manage_principal.setter
    def initial_manage_principal(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "initial_manage_principal", value)

    @property
    @pulumi.getter(name="keyvaultMetadata")
    def keyvault_metadata(self) -> Optional[pulumi.Input['SecretScopeKeyvaultMetadataArgs']]:
        return pulumi.get(self, "keyvault_metadata")

    @keyvault_metadata.setter
    def keyvault_metadata(self, value: Optional[pulumi.Input['SecretScopeKeyvaultMetadataArgs']]):
        pulumi.set(self, "keyvault_metadata", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _SecretScopeState:
    def __init__(__self__, *,
                 backend_type: Optional[pulumi.Input[str]] = None,
                 initial_manage_principal: Optional[pulumi.Input[str]] = None,
                 keyvault_metadata: Optional[pulumi.Input['SecretScopeKeyvaultMetadataArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SecretScope resources.
        """
        if backend_type is not None:
            pulumi.set(__self__, "backend_type", backend_type)
        if initial_manage_principal is not None:
            pulumi.set(__self__, "initial_manage_principal", initial_manage_principal)
        if keyvault_metadata is not None:
            pulumi.set(__self__, "keyvault_metadata", keyvault_metadata)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="backendType")
    def backend_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "backend_type")

    @backend_type.setter
    def backend_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend_type", value)

    @property
    @pulumi.getter(name="initialManagePrincipal")
    def initial_manage_principal(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "initial_manage_principal")

    @initial_manage_principal.setter
    def initial_manage_principal(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "initial_manage_principal", value)

    @property
    @pulumi.getter(name="keyvaultMetadata")
    def keyvault_metadata(self) -> Optional[pulumi.Input['SecretScopeKeyvaultMetadataArgs']]:
        return pulumi.get(self, "keyvault_metadata")

    @keyvault_metadata.setter
    def keyvault_metadata(self, value: Optional[pulumi.Input['SecretScopeKeyvaultMetadataArgs']]):
        pulumi.set(self, "keyvault_metadata", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class SecretScope(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_type: Optional[pulumi.Input[str]] = None,
                 initial_manage_principal: Optional[pulumi.Input[str]] = None,
                 keyvault_metadata: Optional[pulumi.Input[pulumi.InputType['SecretScopeKeyvaultMetadataArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a SecretScope resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SecretScopeArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a SecretScope resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param SecretScopeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecretScopeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_type: Optional[pulumi.Input[str]] = None,
                 initial_manage_principal: Optional[pulumi.Input[str]] = None,
                 keyvault_metadata: Optional[pulumi.Input[pulumi.InputType['SecretScopeKeyvaultMetadataArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecretScopeArgs.__new__(SecretScopeArgs)

            __props__.__dict__["backend_type"] = backend_type
            __props__.__dict__["initial_manage_principal"] = initial_manage_principal
            __props__.__dict__["keyvault_metadata"] = keyvault_metadata
            __props__.__dict__["name"] = name
        super(SecretScope, __self__).__init__(
            'databricks:databricks/secretScope:SecretScope',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backend_type: Optional[pulumi.Input[str]] = None,
            initial_manage_principal: Optional[pulumi.Input[str]] = None,
            keyvault_metadata: Optional[pulumi.Input[pulumi.InputType['SecretScopeKeyvaultMetadataArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'SecretScope':
        """
        Get an existing SecretScope resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SecretScopeState.__new__(_SecretScopeState)

        __props__.__dict__["backend_type"] = backend_type
        __props__.__dict__["initial_manage_principal"] = initial_manage_principal
        __props__.__dict__["keyvault_metadata"] = keyvault_metadata
        __props__.__dict__["name"] = name
        return SecretScope(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backendType")
    def backend_type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "backend_type")

    @property
    @pulumi.getter(name="initialManagePrincipal")
    def initial_manage_principal(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "initial_manage_principal")

    @property
    @pulumi.getter(name="keyvaultMetadata")
    def keyvault_metadata(self) -> pulumi.Output[Optional['outputs.SecretScopeKeyvaultMetadata']]:
        return pulumi.get(self, "keyvault_metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

