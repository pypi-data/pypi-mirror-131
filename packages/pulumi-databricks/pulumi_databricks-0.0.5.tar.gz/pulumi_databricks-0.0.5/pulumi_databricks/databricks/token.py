# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TokenArgs', 'Token']

@pulumi.input_type
class TokenArgs:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 creation_time: Optional[pulumi.Input[int]] = None,
                 expiry_time: Optional[pulumi.Input[int]] = None,
                 lifetime_seconds: Optional[pulumi.Input[int]] = None,
                 token_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Token resource.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if creation_time is not None:
            pulumi.set(__self__, "creation_time", creation_time)
        if expiry_time is not None:
            pulumi.set(__self__, "expiry_time", expiry_time)
        if lifetime_seconds is not None:
            pulumi.set(__self__, "lifetime_seconds", lifetime_seconds)
        if token_id is not None:
            pulumi.set(__self__, "token_id", token_id)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "creation_time")

    @creation_time.setter
    def creation_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "creation_time", value)

    @property
    @pulumi.getter(name="expiryTime")
    def expiry_time(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "expiry_time")

    @expiry_time.setter
    def expiry_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expiry_time", value)

    @property
    @pulumi.getter(name="lifetimeSeconds")
    def lifetime_seconds(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "lifetime_seconds")

    @lifetime_seconds.setter
    def lifetime_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "lifetime_seconds", value)

    @property
    @pulumi.getter(name="tokenId")
    def token_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "token_id")

    @token_id.setter
    def token_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_id", value)


@pulumi.input_type
class _TokenState:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 creation_time: Optional[pulumi.Input[int]] = None,
                 expiry_time: Optional[pulumi.Input[int]] = None,
                 lifetime_seconds: Optional[pulumi.Input[int]] = None,
                 token_id: Optional[pulumi.Input[str]] = None,
                 token_value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Token resources.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if creation_time is not None:
            pulumi.set(__self__, "creation_time", creation_time)
        if expiry_time is not None:
            pulumi.set(__self__, "expiry_time", expiry_time)
        if lifetime_seconds is not None:
            pulumi.set(__self__, "lifetime_seconds", lifetime_seconds)
        if token_id is not None:
            pulumi.set(__self__, "token_id", token_id)
        if token_value is not None:
            pulumi.set(__self__, "token_value", token_value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "creation_time")

    @creation_time.setter
    def creation_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "creation_time", value)

    @property
    @pulumi.getter(name="expiryTime")
    def expiry_time(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "expiry_time")

    @expiry_time.setter
    def expiry_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expiry_time", value)

    @property
    @pulumi.getter(name="lifetimeSeconds")
    def lifetime_seconds(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "lifetime_seconds")

    @lifetime_seconds.setter
    def lifetime_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "lifetime_seconds", value)

    @property
    @pulumi.getter(name="tokenId")
    def token_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "token_id")

    @token_id.setter
    def token_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_id", value)

    @property
    @pulumi.getter(name="tokenValue")
    def token_value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "token_value")

    @token_value.setter
    def token_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_value", value)


class Token(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 creation_time: Optional[pulumi.Input[int]] = None,
                 expiry_time: Optional[pulumi.Input[int]] = None,
                 lifetime_seconds: Optional[pulumi.Input[int]] = None,
                 token_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a Token resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[TokenArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Token resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param TokenArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TokenArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 creation_time: Optional[pulumi.Input[int]] = None,
                 expiry_time: Optional[pulumi.Input[int]] = None,
                 lifetime_seconds: Optional[pulumi.Input[int]] = None,
                 token_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = TokenArgs.__new__(TokenArgs)

            __props__.__dict__["comment"] = comment
            __props__.__dict__["creation_time"] = creation_time
            __props__.__dict__["expiry_time"] = expiry_time
            __props__.__dict__["lifetime_seconds"] = lifetime_seconds
            __props__.__dict__["token_id"] = token_id
            __props__.__dict__["token_value"] = None
        super(Token, __self__).__init__(
            'databricks:databricks/token:Token',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            comment: Optional[pulumi.Input[str]] = None,
            creation_time: Optional[pulumi.Input[int]] = None,
            expiry_time: Optional[pulumi.Input[int]] = None,
            lifetime_seconds: Optional[pulumi.Input[int]] = None,
            token_id: Optional[pulumi.Input[str]] = None,
            token_value: Optional[pulumi.Input[str]] = None) -> 'Token':
        """
        Get an existing Token resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TokenState.__new__(_TokenState)

        __props__.__dict__["comment"] = comment
        __props__.__dict__["creation_time"] = creation_time
        __props__.__dict__["expiry_time"] = expiry_time
        __props__.__dict__["lifetime_seconds"] = lifetime_seconds
        __props__.__dict__["token_id"] = token_id
        __props__.__dict__["token_value"] = token_value
        return Token(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[int]:
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="expiryTime")
    def expiry_time(self) -> pulumi.Output[int]:
        return pulumi.get(self, "expiry_time")

    @property
    @pulumi.getter(name="lifetimeSeconds")
    def lifetime_seconds(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "lifetime_seconds")

    @property
    @pulumi.getter(name="tokenId")
    def token_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "token_id")

    @property
    @pulumi.getter(name="tokenValue")
    def token_value(self) -> pulumi.Output[str]:
        return pulumi.get(self, "token_value")

