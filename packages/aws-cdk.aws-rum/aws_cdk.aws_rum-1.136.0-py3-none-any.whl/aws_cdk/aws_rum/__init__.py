'''
# AWS::RUM Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_rum as rum
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RUM](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RUM.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAppMonitor(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-rum.CfnAppMonitor",
):
    '''A CloudFormation ``AWS::RUM::AppMonitor``.

    :cloudformationResource: AWS::RUM::AppMonitor
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_rum as rum
        
        cfn_app_monitor = rum.CfnAppMonitor(self, "MyCfnAppMonitor",
            app_monitor_configuration=rum.CfnAppMonitor.AppMonitorConfigurationProperty(
                allow_cookies=False,
                enable_xRay=False,
                excluded_pages=["excludedPages"],
                favorite_pages=["favoritePages"],
                guest_role_arn="guestRoleArn",
                identity_pool_id="identityPoolId",
                included_pages=["includedPages"],
                session_sample_rate=123,
                telemetries=["telemetries"]
            ),
            cw_log_enabled=False,
            domain="domain",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        app_monitor_configuration: typing.Optional[typing.Union["CfnAppMonitor.AppMonitorConfigurationProperty", aws_cdk.core.IResolvable]] = None,
        cw_log_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        domain: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::RUM::AppMonitor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_monitor_configuration: ``AWS::RUM::AppMonitor.AppMonitorConfiguration``.
        :param cw_log_enabled: ``AWS::RUM::AppMonitor.CwLogEnabled``.
        :param domain: ``AWS::RUM::AppMonitor.Domain``.
        :param name: ``AWS::RUM::AppMonitor.Name``.
        :param tags: ``AWS::RUM::AppMonitor.Tags``.
        '''
        props = CfnAppMonitorProps(
            app_monitor_configuration=app_monitor_configuration,
            cw_log_enabled=cw_log_enabled,
            domain=domain,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="appMonitorConfiguration")
    def app_monitor_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnAppMonitor.AppMonitorConfigurationProperty", aws_cdk.core.IResolvable]]:
        '''``AWS::RUM::AppMonitor.AppMonitorConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-appmonitorconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAppMonitor.AppMonitorConfigurationProperty", aws_cdk.core.IResolvable]], jsii.get(self, "appMonitorConfiguration"))

    @app_monitor_configuration.setter
    def app_monitor_configuration(
        self,
        value: typing.Optional[typing.Union["CfnAppMonitor.AppMonitorConfigurationProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "appMonitorConfiguration", value)

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cwLogEnabled")
    def cw_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''``AWS::RUM::AppMonitor.CwLogEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-cwlogenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "cwLogEnabled"))

    @cw_log_enabled.setter
    def cw_log_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "cwLogEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''``AWS::RUM::AppMonitor.Domain``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "domain", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RUM::AppMonitor.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::RUM::AppMonitor.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-rum.CfnAppMonitor.AppMonitorConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_cookies": "allowCookies",
            "enable_x_ray": "enableXRay",
            "excluded_pages": "excludedPages",
            "favorite_pages": "favoritePages",
            "guest_role_arn": "guestRoleArn",
            "identity_pool_id": "identityPoolId",
            "included_pages": "includedPages",
            "session_sample_rate": "sessionSampleRate",
            "telemetries": "telemetries",
        },
    )
    class AppMonitorConfigurationProperty:
        def __init__(
            self,
            *,
            allow_cookies: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            enable_x_ray: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            excluded_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
            favorite_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
            guest_role_arn: typing.Optional[builtins.str] = None,
            identity_pool_id: typing.Optional[builtins.str] = None,
            included_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
            session_sample_rate: typing.Optional[jsii.Number] = None,
            telemetries: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param allow_cookies: ``CfnAppMonitor.AppMonitorConfigurationProperty.AllowCookies``.
            :param enable_x_ray: ``CfnAppMonitor.AppMonitorConfigurationProperty.EnableXRay``.
            :param excluded_pages: ``CfnAppMonitor.AppMonitorConfigurationProperty.ExcludedPages``.
            :param favorite_pages: ``CfnAppMonitor.AppMonitorConfigurationProperty.FavoritePages``.
            :param guest_role_arn: ``CfnAppMonitor.AppMonitorConfigurationProperty.GuestRoleArn``.
            :param identity_pool_id: ``CfnAppMonitor.AppMonitorConfigurationProperty.IdentityPoolId``.
            :param included_pages: ``CfnAppMonitor.AppMonitorConfigurationProperty.IncludedPages``.
            :param session_sample_rate: ``CfnAppMonitor.AppMonitorConfigurationProperty.SessionSampleRate``.
            :param telemetries: ``CfnAppMonitor.AppMonitorConfigurationProperty.Telemetries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_rum as rum
                
                app_monitor_configuration_property = rum.CfnAppMonitor.AppMonitorConfigurationProperty(
                    allow_cookies=False,
                    enable_xRay=False,
                    excluded_pages=["excludedPages"],
                    favorite_pages=["favoritePages"],
                    guest_role_arn="guestRoleArn",
                    identity_pool_id="identityPoolId",
                    included_pages=["includedPages"],
                    session_sample_rate=123,
                    telemetries=["telemetries"]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if allow_cookies is not None:
                self._values["allow_cookies"] = allow_cookies
            if enable_x_ray is not None:
                self._values["enable_x_ray"] = enable_x_ray
            if excluded_pages is not None:
                self._values["excluded_pages"] = excluded_pages
            if favorite_pages is not None:
                self._values["favorite_pages"] = favorite_pages
            if guest_role_arn is not None:
                self._values["guest_role_arn"] = guest_role_arn
            if identity_pool_id is not None:
                self._values["identity_pool_id"] = identity_pool_id
            if included_pages is not None:
                self._values["included_pages"] = included_pages
            if session_sample_rate is not None:
                self._values["session_sample_rate"] = session_sample_rate
            if telemetries is not None:
                self._values["telemetries"] = telemetries

        @builtins.property
        def allow_cookies(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.AllowCookies``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-allowcookies
            '''
            result = self._values.get("allow_cookies")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def enable_x_ray(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.EnableXRay``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-enablexray
            '''
            result = self._values.get("enable_x_ray")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def excluded_pages(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.ExcludedPages``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-excludedpages
            '''
            result = self._values.get("excluded_pages")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def favorite_pages(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.FavoritePages``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-favoritepages
            '''
            result = self._values.get("favorite_pages")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def guest_role_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.GuestRoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-guestrolearn
            '''
            result = self._values.get("guest_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[builtins.str]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.IdentityPoolId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-identitypoolid
            '''
            result = self._values.get("identity_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def included_pages(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.IncludedPages``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-includedpages
            '''
            result = self._values.get("included_pages")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def session_sample_rate(self) -> typing.Optional[jsii.Number]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.SessionSampleRate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-sessionsamplerate
            '''
            result = self._values.get("session_sample_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def telemetries(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnAppMonitor.AppMonitorConfigurationProperty.Telemetries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rum-appmonitor-appmonitorconfiguration.html#cfn-rum-appmonitor-appmonitorconfiguration-telemetries
            '''
            result = self._values.get("telemetries")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppMonitorConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-rum.CfnAppMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_monitor_configuration": "appMonitorConfiguration",
        "cw_log_enabled": "cwLogEnabled",
        "domain": "domain",
        "name": "name",
        "tags": "tags",
    },
)
class CfnAppMonitorProps:
    def __init__(
        self,
        *,
        app_monitor_configuration: typing.Optional[typing.Union[CfnAppMonitor.AppMonitorConfigurationProperty, aws_cdk.core.IResolvable]] = None,
        cw_log_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        domain: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::RUM::AppMonitor``.

        :param app_monitor_configuration: ``AWS::RUM::AppMonitor.AppMonitorConfiguration``.
        :param cw_log_enabled: ``AWS::RUM::AppMonitor.CwLogEnabled``.
        :param domain: ``AWS::RUM::AppMonitor.Domain``.
        :param name: ``AWS::RUM::AppMonitor.Name``.
        :param tags: ``AWS::RUM::AppMonitor.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_rum as rum
            
            cfn_app_monitor_props = rum.CfnAppMonitorProps(
                app_monitor_configuration=rum.CfnAppMonitor.AppMonitorConfigurationProperty(
                    allow_cookies=False,
                    enable_xRay=False,
                    excluded_pages=["excludedPages"],
                    favorite_pages=["favoritePages"],
                    guest_role_arn="guestRoleArn",
                    identity_pool_id="identityPoolId",
                    included_pages=["includedPages"],
                    session_sample_rate=123,
                    telemetries=["telemetries"]
                ),
                cw_log_enabled=False,
                domain="domain",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if app_monitor_configuration is not None:
            self._values["app_monitor_configuration"] = app_monitor_configuration
        if cw_log_enabled is not None:
            self._values["cw_log_enabled"] = cw_log_enabled
        if domain is not None:
            self._values["domain"] = domain
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_monitor_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnAppMonitor.AppMonitorConfigurationProperty, aws_cdk.core.IResolvable]]:
        '''``AWS::RUM::AppMonitor.AppMonitorConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-appmonitorconfiguration
        '''
        result = self._values.get("app_monitor_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnAppMonitor.AppMonitorConfigurationProperty, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def cw_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''``AWS::RUM::AppMonitor.CwLogEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-cwlogenabled
        '''
        result = self._values.get("cw_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''``AWS::RUM::AppMonitor.Domain``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RUM::AppMonitor.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::RUM::AppMonitor.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rum-appmonitor.html#cfn-rum-appmonitor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAppMonitor",
    "CfnAppMonitorProps",
]

publication.publish()
