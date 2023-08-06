'''
# AWS::RefactorSpaces Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_refactorspaces as refactorspaces
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RefactorSpaces](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RefactorSpaces.html).

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
class CfnApplication(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnApplication",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Application``.

    :cloudformationResource: AWS::RefactorSpaces::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_application = refactorspaces.CfnApplication(self, "MyCfnApplication",
            api_gateway_proxy=refactorspaces.CfnApplication.ApiGatewayProxyInputProperty(
                endpoint_type="endpointType",
                stage_name="stageName"
            ),
            environment_identifier="environmentIdentifier",
            name="name",
            proxy_type="proxyType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_id="vpcId"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        api_gateway_proxy: typing.Optional[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", aws_cdk.core.IResolvable]] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_gateway_proxy: ``AWS::RefactorSpaces::Application.ApiGatewayProxy``.
        :param environment_identifier: ``AWS::RefactorSpaces::Application.EnvironmentIdentifier``.
        :param name: ``AWS::RefactorSpaces::Application.Name``.
        :param proxy_type: ``AWS::RefactorSpaces::Application.ProxyType``.
        :param tags: ``AWS::RefactorSpaces::Application.Tags``.
        :param vpc_id: ``AWS::RefactorSpaces::Application.VpcId``.
        '''
        props = CfnApplicationProps(
            api_gateway_proxy=api_gateway_proxy,
            environment_identifier=environment_identifier,
            name=name,
            proxy_type=proxy_type,
            tags=tags,
            vpc_id=vpc_id,
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
    @jsii.member(jsii_name="apiGatewayProxy")
    def api_gateway_proxy(
        self,
    ) -> typing.Optional[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", aws_cdk.core.IResolvable]]:
        '''``AWS::RefactorSpaces::Application.ApiGatewayProxy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-apigatewayproxy
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", aws_cdk.core.IResolvable]], jsii.get(self, "apiGatewayProxy"))

    @api_gateway_proxy.setter
    def api_gateway_proxy(
        self,
        value: typing.Optional[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "apiGatewayProxy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrApiGatewayId")
    def attr_api_gateway_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ApiGatewayId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApiGatewayId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrApplicationIdentifier")
    def attr_application_identifier(self) -> builtins.str:
        '''
        :cloudformationAttribute: ApplicationIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrNlbArn")
    def attr_nlb_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: NlbArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNlbArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrNlbName")
    def attr_nlb_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: NlbName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNlbName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrProxyUrl")
    def attr_proxy_url(self) -> builtins.str:
        '''
        :cloudformationAttribute: ProxyUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProxyUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrStageName")
    def attr_stage_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: StageName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStageName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVpcLinkId")
    def attr_vpc_link_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: VpcLinkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcLinkId"))

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
    @jsii.member(jsii_name="environmentIdentifier")
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.EnvironmentIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-environmentidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentIdentifier"))

    @environment_identifier.setter
    def environment_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "environmentIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="proxyType")
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.ProxyType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-proxytype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyType"))

    @proxy_type.setter
    def proxy_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "proxyType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::RefactorSpaces::Application.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-vpcid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "vpcId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnApplication.ApiGatewayProxyInputProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "stage_name": "stageName"},
    )
    class ApiGatewayProxyInputProperty:
        def __init__(
            self,
            *,
            endpoint_type: typing.Optional[builtins.str] = None,
            stage_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param endpoint_type: ``CfnApplication.ApiGatewayProxyInputProperty.EndpointType``.
            :param stage_name: ``CfnApplication.ApiGatewayProxyInputProperty.StageName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                api_gateway_proxy_input_property = refactorspaces.CfnApplication.ApiGatewayProxyInputProperty(
                    endpoint_type="endpointType",
                    stage_name="stageName"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if stage_name is not None:
                self._values["stage_name"] = stage_name

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            '''``CfnApplication.ApiGatewayProxyInputProperty.EndpointType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html#cfn-refactorspaces-application-apigatewayproxyinput-endpointtype
            '''
            result = self._values.get("endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApplication.ApiGatewayProxyInputProperty.StageName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html#cfn-refactorspaces-application-apigatewayproxyinput-stagename
            '''
            result = self._values.get("stage_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiGatewayProxyInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_gateway_proxy": "apiGatewayProxy",
        "environment_identifier": "environmentIdentifier",
        "name": "name",
        "proxy_type": "proxyType",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        api_gateway_proxy: typing.Optional[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, aws_cdk.core.IResolvable]] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::RefactorSpaces::Application``.

        :param api_gateway_proxy: ``AWS::RefactorSpaces::Application.ApiGatewayProxy``.
        :param environment_identifier: ``AWS::RefactorSpaces::Application.EnvironmentIdentifier``.
        :param name: ``AWS::RefactorSpaces::Application.Name``.
        :param proxy_type: ``AWS::RefactorSpaces::Application.ProxyType``.
        :param tags: ``AWS::RefactorSpaces::Application.Tags``.
        :param vpc_id: ``AWS::RefactorSpaces::Application.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_application_props = refactorspaces.CfnApplicationProps(
                api_gateway_proxy=refactorspaces.CfnApplication.ApiGatewayProxyInputProperty(
                    endpoint_type="endpointType",
                    stage_name="stageName"
                ),
                environment_identifier="environmentIdentifier",
                name="name",
                proxy_type="proxyType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_id="vpcId"
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if api_gateway_proxy is not None:
            self._values["api_gateway_proxy"] = api_gateway_proxy
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if name is not None:
            self._values["name"] = name
        if proxy_type is not None:
            self._values["proxy_type"] = proxy_type
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def api_gateway_proxy(
        self,
    ) -> typing.Optional[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, aws_cdk.core.IResolvable]]:
        '''``AWS::RefactorSpaces::Application.ApiGatewayProxy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-apigatewayproxy
        '''
        result = self._values.get("api_gateway_proxy")
        return typing.cast(typing.Optional[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.EnvironmentIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.ProxyType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-proxytype
        '''
        result = self._values.get("proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::RefactorSpaces::Application.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Application.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEnvironment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnEnvironment",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Environment``.

    :cloudformationResource: AWS::RefactorSpaces::Environment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_environment = refactorspaces.CfnEnvironment(self, "MyCfnEnvironment",
            description="description",
            name="name",
            network_fabric_type="networkFabricType",
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
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_fabric_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::RefactorSpaces::Environment.Description``.
        :param name: ``AWS::RefactorSpaces::Environment.Name``.
        :param network_fabric_type: ``AWS::RefactorSpaces::Environment.NetworkFabricType``.
        :param tags: ``AWS::RefactorSpaces::Environment.Tags``.
        '''
        props = CfnEnvironmentProps(
            description=description,
            name=name,
            network_fabric_type=network_fabric_type,
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrEnvironmentIdentifier")
    def attr_environment_identifier(self) -> builtins.str:
        '''
        :cloudformationAttribute: EnvironmentIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrTransitGatewayId")
    def attr_transit_gateway_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: TransitGatewayId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTransitGatewayId"))

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
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Environment.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Environment.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="networkFabricType")
    def network_fabric_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Environment.NetworkFabricType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-networkfabrictype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkFabricType"))

    @network_fabric_type.setter
    def network_fabric_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "networkFabricType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::RefactorSpaces::Environment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "network_fabric_type": "networkFabricType",
        "tags": "tags",
    },
)
class CfnEnvironmentProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_fabric_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::RefactorSpaces::Environment``.

        :param description: ``AWS::RefactorSpaces::Environment.Description``.
        :param name: ``AWS::RefactorSpaces::Environment.Name``.
        :param network_fabric_type: ``AWS::RefactorSpaces::Environment.NetworkFabricType``.
        :param tags: ``AWS::RefactorSpaces::Environment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_environment_props = refactorspaces.CfnEnvironmentProps(
                description="description",
                name="name",
                network_fabric_type="networkFabricType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if network_fabric_type is not None:
            self._values["network_fabric_type"] = network_fabric_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Environment.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Environment.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_fabric_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Environment.NetworkFabricType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-networkfabrictype
        '''
        result = self._values.get("network_fabric_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::RefactorSpaces::Environment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRoute(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnRoute",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Route``.

    :cloudformationResource: AWS::RefactorSpaces::Route
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_route = refactorspaces.CfnRoute(self, "MyCfnRoute",
            application_identifier="applicationIdentifier",
            environment_identifier="environmentIdentifier",
            service_identifier="serviceIdentifier",
        
            # the properties below are optional
            route_type="routeType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            uri_path_route=refactorspaces.CfnRoute.UriPathRouteInputProperty(
                activation_state="activationState",
        
                # the properties below are optional
                include_child_paths=False,
                methods=["methods"],
                source_path="sourcePath"
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        application_identifier: builtins.str,
        environment_identifier: builtins.str,
        route_type: typing.Optional[builtins.str] = None,
        service_identifier: builtins.str,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        uri_path_route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.UriPathRouteInputProperty"]] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_identifier: ``AWS::RefactorSpaces::Route.ApplicationIdentifier``.
        :param environment_identifier: ``AWS::RefactorSpaces::Route.EnvironmentIdentifier``.
        :param route_type: ``AWS::RefactorSpaces::Route.RouteType``.
        :param service_identifier: ``AWS::RefactorSpaces::Route.ServiceIdentifier``.
        :param tags: ``AWS::RefactorSpaces::Route.Tags``.
        :param uri_path_route: ``AWS::RefactorSpaces::Route.UriPathRoute``.
        '''
        props = CfnRouteProps(
            application_identifier=application_identifier,
            environment_identifier=environment_identifier,
            route_type=route_type,
            service_identifier=service_identifier,
            tags=tags,
            uri_path_route=uri_path_route,
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
    @jsii.member(jsii_name="applicationIdentifier")
    def application_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Route.ApplicationIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-applicationidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationIdentifier"))

    @application_identifier.setter
    def application_identifier(self, value: builtins.str) -> None:
        jsii.set(self, "applicationIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrPathResourceToId")
    def attr_path_resource_to_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: PathResourceToId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPathResourceToId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrRouteIdentifier")
    def attr_route_identifier(self) -> builtins.str:
        '''
        :cloudformationAttribute: RouteIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRouteIdentifier"))

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
    @jsii.member(jsii_name="environmentIdentifier")
    def environment_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Route.EnvironmentIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-environmentidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentIdentifier"))

    @environment_identifier.setter
    def environment_identifier(self, value: builtins.str) -> None:
        jsii.set(self, "environmentIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="routeType")
    def route_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Route.RouteType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-routetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeType"))

    @route_type.setter
    def route_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "routeType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Route.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-serviceidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: builtins.str) -> None:
        jsii.set(self, "serviceIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::RefactorSpaces::Route.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="uriPathRoute")
    def uri_path_route(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.UriPathRouteInputProperty"]]:
        '''``AWS::RefactorSpaces::Route.UriPathRoute``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-uripathroute
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.UriPathRouteInputProperty"]], jsii.get(self, "uriPathRoute"))

    @uri_path_route.setter
    def uri_path_route(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRoute.UriPathRouteInputProperty"]],
    ) -> None:
        jsii.set(self, "uriPathRoute", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnRoute.UriPathRouteInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "activation_state": "activationState",
            "include_child_paths": "includeChildPaths",
            "methods": "methods",
            "source_path": "sourcePath",
        },
    )
    class UriPathRouteInputProperty:
        def __init__(
            self,
            *,
            activation_state: builtins.str,
            include_child_paths: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param activation_state: ``CfnRoute.UriPathRouteInputProperty.ActivationState``.
            :param include_child_paths: ``CfnRoute.UriPathRouteInputProperty.IncludeChildPaths``.
            :param methods: ``CfnRoute.UriPathRouteInputProperty.Methods``.
            :param source_path: ``CfnRoute.UriPathRouteInputProperty.SourcePath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                uri_path_route_input_property = refactorspaces.CfnRoute.UriPathRouteInputProperty(
                    activation_state="activationState",
                
                    # the properties below are optional
                    include_child_paths=False,
                    methods=["methods"],
                    source_path="sourcePath"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "activation_state": activation_state,
            }
            if include_child_paths is not None:
                self._values["include_child_paths"] = include_child_paths
            if methods is not None:
                self._values["methods"] = methods
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def activation_state(self) -> builtins.str:
            '''``CfnRoute.UriPathRouteInputProperty.ActivationState``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-activationstate
            '''
            result = self._values.get("activation_state")
            assert result is not None, "Required property 'activation_state' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def include_child_paths(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnRoute.UriPathRouteInputProperty.IncludeChildPaths``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-includechildpaths
            '''
            result = self._values.get("include_child_paths")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRoute.UriPathRouteInputProperty.Methods``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-methods
            '''
            result = self._values.get("methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''``CfnRoute.UriPathRouteInputProperty.SourcePath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UriPathRouteInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnRouteProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "environment_identifier": "environmentIdentifier",
        "route_type": "routeType",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
        "uri_path_route": "uriPathRoute",
    },
)
class CfnRouteProps:
    def __init__(
        self,
        *,
        application_identifier: builtins.str,
        environment_identifier: builtins.str,
        route_type: typing.Optional[builtins.str] = None,
        service_identifier: builtins.str,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        uri_path_route: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRoute.UriPathRouteInputProperty]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::RefactorSpaces::Route``.

        :param application_identifier: ``AWS::RefactorSpaces::Route.ApplicationIdentifier``.
        :param environment_identifier: ``AWS::RefactorSpaces::Route.EnvironmentIdentifier``.
        :param route_type: ``AWS::RefactorSpaces::Route.RouteType``.
        :param service_identifier: ``AWS::RefactorSpaces::Route.ServiceIdentifier``.
        :param tags: ``AWS::RefactorSpaces::Route.Tags``.
        :param uri_path_route: ``AWS::RefactorSpaces::Route.UriPathRoute``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_route_props = refactorspaces.CfnRouteProps(
                application_identifier="applicationIdentifier",
                environment_identifier="environmentIdentifier",
                service_identifier="serviceIdentifier",
            
                # the properties below are optional
                route_type="routeType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                uri_path_route=refactorspaces.CfnRoute.UriPathRouteInputProperty(
                    activation_state="activationState",
            
                    # the properties below are optional
                    include_child_paths=False,
                    methods=["methods"],
                    source_path="sourcePath"
                )
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_identifier": application_identifier,
            "environment_identifier": environment_identifier,
            "service_identifier": service_identifier,
        }
        if route_type is not None:
            self._values["route_type"] = route_type
        if tags is not None:
            self._values["tags"] = tags
        if uri_path_route is not None:
            self._values["uri_path_route"] = uri_path_route

    @builtins.property
    def application_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Route.ApplicationIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        assert result is not None, "Required property 'application_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Route.EnvironmentIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        assert result is not None, "Required property 'environment_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Route.RouteType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-routetype
        '''
        result = self._values.get("route_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Route.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        assert result is not None, "Required property 'service_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::RefactorSpaces::Route.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def uri_path_route(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRoute.UriPathRouteInputProperty]]:
        '''``AWS::RefactorSpaces::Route.UriPathRoute``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-uripathroute
        '''
        result = self._values.get("uri_path_route")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRoute.UriPathRouteInputProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnService(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnService",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Service``.

    :cloudformationResource: AWS::RefactorSpaces::Service
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_service = refactorspaces.CfnService(self, "MyCfnService",
            application_identifier="applicationIdentifier",
            environment_identifier="environmentIdentifier",
        
            # the properties below are optional
            description="description",
            endpoint_type="endpointType",
            lambda_endpoint=refactorspaces.CfnService.LambdaEndpointInputProperty(
                arn="arn"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            url_endpoint=refactorspaces.CfnService.UrlEndpointInputProperty(
                url="url",
        
                # the properties below are optional
                health_url="healthUrl"
            ),
            vpc_id="vpcId"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        application_identifier: builtins.str,
        description: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        environment_identifier: builtins.str,
        lambda_endpoint: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.LambdaEndpointInputProperty"]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        url_endpoint: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.UrlEndpointInputProperty"]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_identifier: ``AWS::RefactorSpaces::Service.ApplicationIdentifier``.
        :param description: ``AWS::RefactorSpaces::Service.Description``.
        :param endpoint_type: ``AWS::RefactorSpaces::Service.EndpointType``.
        :param environment_identifier: ``AWS::RefactorSpaces::Service.EnvironmentIdentifier``.
        :param lambda_endpoint: ``AWS::RefactorSpaces::Service.LambdaEndpoint``.
        :param name: ``AWS::RefactorSpaces::Service.Name``.
        :param tags: ``AWS::RefactorSpaces::Service.Tags``.
        :param url_endpoint: ``AWS::RefactorSpaces::Service.UrlEndpoint``.
        :param vpc_id: ``AWS::RefactorSpaces::Service.VpcId``.
        '''
        props = CfnServiceProps(
            application_identifier=application_identifier,
            description=description,
            endpoint_type=endpoint_type,
            environment_identifier=environment_identifier,
            lambda_endpoint=lambda_endpoint,
            name=name,
            tags=tags,
            url_endpoint=url_endpoint,
            vpc_id=vpc_id,
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
    @jsii.member(jsii_name="applicationIdentifier")
    def application_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Service.ApplicationIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-applicationidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationIdentifier"))

    @application_identifier.setter
    def application_identifier(self, value: builtins.str) -> None:
        jsii.set(self, "applicationIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrServiceIdentifier")
    def attr_service_identifier(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceIdentifier"))

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
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.EndpointType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-endpointtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "endpointType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="environmentIdentifier")
    def environment_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Service.EnvironmentIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-environmentidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentIdentifier"))

    @environment_identifier.setter
    def environment_identifier(self, value: builtins.str) -> None:
        jsii.set(self, "environmentIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaEndpoint")
    def lambda_endpoint(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.LambdaEndpointInputProperty"]]:
        '''``AWS::RefactorSpaces::Service.LambdaEndpoint``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-lambdaendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.LambdaEndpointInputProperty"]], jsii.get(self, "lambdaEndpoint"))

    @lambda_endpoint.setter
    def lambda_endpoint(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.LambdaEndpointInputProperty"]],
    ) -> None:
        jsii.set(self, "lambdaEndpoint", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::RefactorSpaces::Service.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="urlEndpoint")
    def url_endpoint(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.UrlEndpointInputProperty"]]:
        '''``AWS::RefactorSpaces::Service.UrlEndpoint``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-urlendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.UrlEndpointInputProperty"]], jsii.get(self, "urlEndpoint"))

    @url_endpoint.setter
    def url_endpoint(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnService.UrlEndpointInputProperty"]],
    ) -> None:
        jsii.set(self, "urlEndpoint", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-vpcid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "vpcId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnService.LambdaEndpointInputProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class LambdaEndpointInputProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''
            :param arn: ``CfnService.LambdaEndpointInputProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-lambdaendpointinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                lambda_endpoint_input_property = refactorspaces.CfnService.LambdaEndpointInputProperty(
                    arn="arn"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''``CfnService.LambdaEndpointInputProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-lambdaendpointinput.html#cfn-refactorspaces-service-lambdaendpointinput-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaEndpointInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnService.UrlEndpointInputProperty",
        jsii_struct_bases=[],
        name_mapping={"health_url": "healthUrl", "url": "url"},
    )
    class UrlEndpointInputProperty:
        def __init__(
            self,
            *,
            health_url: typing.Optional[builtins.str] = None,
            url: builtins.str,
        ) -> None:
            '''
            :param health_url: ``CfnService.UrlEndpointInputProperty.HealthUrl``.
            :param url: ``CfnService.UrlEndpointInputProperty.Url``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                url_endpoint_input_property = refactorspaces.CfnService.UrlEndpointInputProperty(
                    url="url",
                
                    # the properties below are optional
                    health_url="healthUrl"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "url": url,
            }
            if health_url is not None:
                self._values["health_url"] = health_url

        @builtins.property
        def health_url(self) -> typing.Optional[builtins.str]:
            '''``CfnService.UrlEndpointInputProperty.HealthUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html#cfn-refactorspaces-service-urlendpointinput-healthurl
            '''
            result = self._values.get("health_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> builtins.str:
            '''``CfnService.UrlEndpointInputProperty.Url``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html#cfn-refactorspaces-service-urlendpointinput-url
            '''
            result = self._values.get("url")
            assert result is not None, "Required property 'url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UrlEndpointInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "description": "description",
        "endpoint_type": "endpointType",
        "environment_identifier": "environmentIdentifier",
        "lambda_endpoint": "lambdaEndpoint",
        "name": "name",
        "tags": "tags",
        "url_endpoint": "urlEndpoint",
        "vpc_id": "vpcId",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        application_identifier: builtins.str,
        description: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        environment_identifier: builtins.str,
        lambda_endpoint: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnService.LambdaEndpointInputProperty]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
        url_endpoint: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnService.UrlEndpointInputProperty]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::RefactorSpaces::Service``.

        :param application_identifier: ``AWS::RefactorSpaces::Service.ApplicationIdentifier``.
        :param description: ``AWS::RefactorSpaces::Service.Description``.
        :param endpoint_type: ``AWS::RefactorSpaces::Service.EndpointType``.
        :param environment_identifier: ``AWS::RefactorSpaces::Service.EnvironmentIdentifier``.
        :param lambda_endpoint: ``AWS::RefactorSpaces::Service.LambdaEndpoint``.
        :param name: ``AWS::RefactorSpaces::Service.Name``.
        :param tags: ``AWS::RefactorSpaces::Service.Tags``.
        :param url_endpoint: ``AWS::RefactorSpaces::Service.UrlEndpoint``.
        :param vpc_id: ``AWS::RefactorSpaces::Service.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_service_props = refactorspaces.CfnServiceProps(
                application_identifier="applicationIdentifier",
                environment_identifier="environmentIdentifier",
            
                # the properties below are optional
                description="description",
                endpoint_type="endpointType",
                lambda_endpoint=refactorspaces.CfnService.LambdaEndpointInputProperty(
                    arn="arn"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                url_endpoint=refactorspaces.CfnService.UrlEndpointInputProperty(
                    url="url",
            
                    # the properties below are optional
                    health_url="healthUrl"
                ),
                vpc_id="vpcId"
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_identifier": application_identifier,
            "environment_identifier": environment_identifier,
        }
        if description is not None:
            self._values["description"] = description
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if lambda_endpoint is not None:
            self._values["lambda_endpoint"] = lambda_endpoint
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if url_endpoint is not None:
            self._values["url_endpoint"] = url_endpoint
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def application_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Service.ApplicationIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        assert result is not None, "Required property 'application_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.EndpointType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-endpointtype
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_identifier(self) -> builtins.str:
        '''``AWS::RefactorSpaces::Service.EnvironmentIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        assert result is not None, "Required property 'environment_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_endpoint(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnService.LambdaEndpointInputProperty]]:
        '''``AWS::RefactorSpaces::Service.LambdaEndpoint``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-lambdaendpoint
        '''
        result = self._values.get("lambda_endpoint")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnService.LambdaEndpointInputProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::RefactorSpaces::Service.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    @builtins.property
    def url_endpoint(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnService.UrlEndpointInputProperty]]:
        '''``AWS::RefactorSpaces::Service.UrlEndpoint``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-urlendpoint
        '''
        result = self._values.get("url_endpoint")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnService.UrlEndpointInputProperty]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RefactorSpaces::Service.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnEnvironment",
    "CfnEnvironmentProps",
    "CfnRoute",
    "CfnRouteProps",
    "CfnService",
    "CfnServiceProps",
]

publication.publish()
