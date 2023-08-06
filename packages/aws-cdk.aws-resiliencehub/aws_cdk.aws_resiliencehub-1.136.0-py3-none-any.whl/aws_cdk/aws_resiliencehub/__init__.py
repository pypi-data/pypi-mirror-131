'''
# AWS::ResilienceHub Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_resiliencehub as resiliencehub
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ResilienceHub](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResilienceHub.html).

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
class CfnApp(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-resiliencehub.CfnApp",
):
    '''A CloudFormation ``AWS::ResilienceHub::App``.

    :cloudformationResource: AWS::ResilienceHub::App
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_resiliencehub as resiliencehub
        
        cfn_app = resiliencehub.CfnApp(self, "MyCfnApp",
            app_template_body="appTemplateBody",
            name="name",
            resource_mappings=[resiliencehub.CfnApp.ResourceMappingProperty(
                mapping_type="mappingType",
                physical_resource_id=resiliencehub.CfnApp.PhysicalResourceIdProperty(
                    identifier="identifier",
                    type="type",
        
                    # the properties below are optional
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion"
                ),
        
                # the properties below are optional
                logical_stack_name="logicalStackName",
                resource_name="resourceName"
            )],
        
            # the properties below are optional
            description="description",
            resiliency_policy_arn="resiliencyPolicyArn",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        app_template_body: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: builtins.str,
        resiliency_policy_arn: typing.Optional[builtins.str] = None,
        resource_mappings: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnApp.ResourceMappingProperty"]]],
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHub::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_template_body: ``AWS::ResilienceHub::App.AppTemplateBody``.
        :param description: ``AWS::ResilienceHub::App.Description``.
        :param name: ``AWS::ResilienceHub::App.Name``.
        :param resiliency_policy_arn: ``AWS::ResilienceHub::App.ResiliencyPolicyArn``.
        :param resource_mappings: ``AWS::ResilienceHub::App.ResourceMappings``.
        :param tags: ``AWS::ResilienceHub::App.Tags``.
        '''
        props = CfnAppProps(
            app_template_body=app_template_body,
            description=description,
            name=name,
            resiliency_policy_arn=resiliency_policy_arn,
            resource_mappings=resource_mappings,
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
    @jsii.member(jsii_name="appTemplateBody")
    def app_template_body(self) -> builtins.str:
        '''``AWS::ResilienceHub::App.AppTemplateBody``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-apptemplatebody
        '''
        return typing.cast(builtins.str, jsii.get(self, "appTemplateBody"))

    @app_template_body.setter
    def app_template_body(self, value: builtins.str) -> None:
        jsii.set(self, "appTemplateBody", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAppArn")
    def attr_app_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AppArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppArn"))

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
        '''``AWS::ResilienceHub::App.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::ResilienceHub::App.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resiliencyPolicyArn")
    def resiliency_policy_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::ResilienceHub::App.ResiliencyPolicyArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resiliencypolicyarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resiliencyPolicyArn"))

    @resiliency_policy_arn.setter
    def resiliency_policy_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "resiliencyPolicyArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resourceMappings")
    def resource_mappings(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.ResourceMappingProperty"]]]:
        '''``AWS::ResilienceHub::App.ResourceMappings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resourcemappings
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.ResourceMappingProperty"]]], jsii.get(self, "resourceMappings"))

    @resource_mappings.setter
    def resource_mappings(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.ResourceMappingProperty"]]],
    ) -> None:
        jsii.set(self, "resourceMappings", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::ResilienceHub::App.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resiliencehub.CfnApp.PhysicalResourceIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_id": "awsAccountId",
            "aws_region": "awsRegion",
            "identifier": "identifier",
            "type": "type",
        },
    )
    class PhysicalResourceIdProperty:
        def __init__(
            self,
            *,
            aws_account_id: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            identifier: builtins.str,
            type: builtins.str,
        ) -> None:
            '''
            :param aws_account_id: ``CfnApp.PhysicalResourceIdProperty.AwsAccountId``.
            :param aws_region: ``CfnApp.PhysicalResourceIdProperty.AwsRegion``.
            :param identifier: ``CfnApp.PhysicalResourceIdProperty.Identifier``.
            :param type: ``CfnApp.PhysicalResourceIdProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resiliencehub as resiliencehub
                
                physical_resource_id_property = resiliencehub.CfnApp.PhysicalResourceIdProperty(
                    identifier="identifier",
                    type="type",
                
                    # the properties below are optional
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "identifier": identifier,
                "type": type,
            }
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id
            if aws_region is not None:
                self._values["aws_region"] = aws_region

        @builtins.property
        def aws_account_id(self) -> typing.Optional[builtins.str]:
            '''``CfnApp.PhysicalResourceIdProperty.AwsAccountId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''``CfnApp.PhysicalResourceIdProperty.AwsRegion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identifier(self) -> builtins.str:
            '''``CfnApp.PhysicalResourceIdProperty.Identifier``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-identifier
            '''
            result = self._values.get("identifier")
            assert result is not None, "Required property 'identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnApp.PhysicalResourceIdProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhysicalResourceIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resiliencehub.CfnApp.ResourceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "logical_stack_name": "logicalStackName",
            "mapping_type": "mappingType",
            "physical_resource_id": "physicalResourceId",
            "resource_name": "resourceName",
        },
    )
    class ResourceMappingProperty:
        def __init__(
            self,
            *,
            logical_stack_name: typing.Optional[builtins.str] = None,
            mapping_type: builtins.str,
            physical_resource_id: typing.Union[aws_cdk.core.IResolvable, "CfnApp.PhysicalResourceIdProperty"],
            resource_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param logical_stack_name: ``CfnApp.ResourceMappingProperty.LogicalStackName``.
            :param mapping_type: ``CfnApp.ResourceMappingProperty.MappingType``.
            :param physical_resource_id: ``CfnApp.ResourceMappingProperty.PhysicalResourceId``.
            :param resource_name: ``CfnApp.ResourceMappingProperty.ResourceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resiliencehub as resiliencehub
                
                resource_mapping_property = resiliencehub.CfnApp.ResourceMappingProperty(
                    mapping_type="mappingType",
                    physical_resource_id=resiliencehub.CfnApp.PhysicalResourceIdProperty(
                        identifier="identifier",
                        type="type",
                
                        # the properties below are optional
                        aws_account_id="awsAccountId",
                        aws_region="awsRegion"
                    ),
                
                    # the properties below are optional
                    logical_stack_name="logicalStackName",
                    resource_name="resourceName"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "mapping_type": mapping_type,
                "physical_resource_id": physical_resource_id,
            }
            if logical_stack_name is not None:
                self._values["logical_stack_name"] = logical_stack_name
            if resource_name is not None:
                self._values["resource_name"] = resource_name

        @builtins.property
        def logical_stack_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApp.ResourceMappingProperty.LogicalStackName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-logicalstackname
            '''
            result = self._values.get("logical_stack_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mapping_type(self) -> builtins.str:
            '''``CfnApp.ResourceMappingProperty.MappingType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-mappingtype
            '''
            result = self._values.get("mapping_type")
            assert result is not None, "Required property 'mapping_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def physical_resource_id(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnApp.PhysicalResourceIdProperty"]:
            '''``CfnApp.ResourceMappingProperty.PhysicalResourceId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-physicalresourceid
            '''
            result = self._values.get("physical_resource_id")
            assert result is not None, "Required property 'physical_resource_id' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnApp.PhysicalResourceIdProperty"], result)

        @builtins.property
        def resource_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApp.ResourceMappingProperty.ResourceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-resourcename
            '''
            result = self._values.get("resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-resiliencehub.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_template_body": "appTemplateBody",
        "description": "description",
        "name": "name",
        "resiliency_policy_arn": "resiliencyPolicyArn",
        "resource_mappings": "resourceMappings",
        "tags": "tags",
    },
)
class CfnAppProps:
    def __init__(
        self,
        *,
        app_template_body: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: builtins.str,
        resiliency_policy_arn: typing.Optional[builtins.str] = None,
        resource_mappings: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnApp.ResourceMappingProperty]]],
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::ResilienceHub::App``.

        :param app_template_body: ``AWS::ResilienceHub::App.AppTemplateBody``.
        :param description: ``AWS::ResilienceHub::App.Description``.
        :param name: ``AWS::ResilienceHub::App.Name``.
        :param resiliency_policy_arn: ``AWS::ResilienceHub::App.ResiliencyPolicyArn``.
        :param resource_mappings: ``AWS::ResilienceHub::App.ResourceMappings``.
        :param tags: ``AWS::ResilienceHub::App.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_resiliencehub as resiliencehub
            
            cfn_app_props = resiliencehub.CfnAppProps(
                app_template_body="appTemplateBody",
                name="name",
                resource_mappings=[resiliencehub.CfnApp.ResourceMappingProperty(
                    mapping_type="mappingType",
                    physical_resource_id=resiliencehub.CfnApp.PhysicalResourceIdProperty(
                        identifier="identifier",
                        type="type",
            
                        # the properties below are optional
                        aws_account_id="awsAccountId",
                        aws_region="awsRegion"
                    ),
            
                    # the properties below are optional
                    logical_stack_name="logicalStackName",
                    resource_name="resourceName"
                )],
            
                # the properties below are optional
                description="description",
                resiliency_policy_arn="resiliencyPolicyArn",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "app_template_body": app_template_body,
            "name": name,
            "resource_mappings": resource_mappings,
        }
        if description is not None:
            self._values["description"] = description
        if resiliency_policy_arn is not None:
            self._values["resiliency_policy_arn"] = resiliency_policy_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_template_body(self) -> builtins.str:
        '''``AWS::ResilienceHub::App.AppTemplateBody``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-apptemplatebody
        '''
        result = self._values.get("app_template_body")
        assert result is not None, "Required property 'app_template_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::ResilienceHub::App.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::ResilienceHub::App.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resiliency_policy_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::ResilienceHub::App.ResiliencyPolicyArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resiliencypolicyarn
        '''
        result = self._values.get("resiliency_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_mappings(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApp.ResourceMappingProperty]]]:
        '''``AWS::ResilienceHub::App.ResourceMappings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resourcemappings
        '''
        result = self._values.get("resource_mappings")
        assert result is not None, "Required property 'resource_mappings' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApp.ResourceMappingProperty]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::ResilienceHub::App.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnResiliencyPolicy(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-resiliencehub.CfnResiliencyPolicy",
):
    '''A CloudFormation ``AWS::ResilienceHub::ResiliencyPolicy``.

    :cloudformationResource: AWS::ResilienceHub::ResiliencyPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_resiliencehub as resiliencehub
        
        cfn_resiliency_policy = resiliencehub.CfnResiliencyPolicy(self, "MyCfnResiliencyPolicy",
            policy={
                "policy_key": resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty(
                    rpo_in_secs=123,
                    rto_in_secs=123
                )
            },
            policy_name="policyName",
            tier="tier",
        
            # the properties below are optional
            data_location_constraint="dataLocationConstraint",
            policy_description="policyDescription",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        data_location_constraint: typing.Optional[builtins.str] = None,
        policy: typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnResiliencyPolicy.FailurePolicyProperty"]], aws_cdk.core.IResolvable],
        policy_description: typing.Optional[builtins.str] = None,
        policy_name: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tier: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ResilienceHub::ResiliencyPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_location_constraint: ``AWS::ResilienceHub::ResiliencyPolicy.DataLocationConstraint``.
        :param policy: ``AWS::ResilienceHub::ResiliencyPolicy.Policy``.
        :param policy_description: ``AWS::ResilienceHub::ResiliencyPolicy.PolicyDescription``.
        :param policy_name: ``AWS::ResilienceHub::ResiliencyPolicy.PolicyName``.
        :param tags: ``AWS::ResilienceHub::ResiliencyPolicy.Tags``.
        :param tier: ``AWS::ResilienceHub::ResiliencyPolicy.Tier``.
        '''
        props = CfnResiliencyPolicyProps(
            data_location_constraint=data_location_constraint,
            policy=policy,
            policy_description=policy_description,
            policy_name=policy_name,
            tags=tags,
            tier=tier,
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
    @jsii.member(jsii_name="attrPolicyArn")
    def attr_policy_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: PolicyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPolicyArn"))

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
    @jsii.member(jsii_name="dataLocationConstraint")
    def data_location_constraint(self) -> typing.Optional[builtins.str]:
        '''``AWS::ResilienceHub::ResiliencyPolicy.DataLocationConstraint``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-datalocationconstraint
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataLocationConstraint"))

    @data_location_constraint.setter
    def data_location_constraint(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dataLocationConstraint", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnResiliencyPolicy.FailurePolicyProperty"]]]:
        '''``AWS::ResilienceHub::ResiliencyPolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policy
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnResiliencyPolicy.FailurePolicyProperty"]]], jsii.get(self, "policy"))

    @policy.setter
    def policy(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnResiliencyPolicy.FailurePolicyProperty"]]],
    ) -> None:
        jsii.set(self, "policy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyDescription")
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::ResilienceHub::ResiliencyPolicy.PolicyDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policydescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDescription"))

    @policy_description.setter
    def policy_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "policyDescription", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''``AWS::ResilienceHub::ResiliencyPolicy.PolicyName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        jsii.set(self, "policyName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::ResilienceHub::ResiliencyPolicy.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        '''``AWS::ResilienceHub::ResiliencyPolicy.Tier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tier
        '''
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        jsii.set(self, "tier", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"rpo_in_secs": "rpoInSecs", "rto_in_secs": "rtoInSecs"},
    )
    class FailurePolicyProperty:
        def __init__(
            self,
            *,
            rpo_in_secs: jsii.Number,
            rto_in_secs: jsii.Number,
        ) -> None:
            '''
            :param rpo_in_secs: ``CfnResiliencyPolicy.FailurePolicyProperty.RpoInSecs``.
            :param rto_in_secs: ``CfnResiliencyPolicy.FailurePolicyProperty.RtoInSecs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resiliencehub as resiliencehub
                
                failure_policy_property = resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty(
                    rpo_in_secs=123,
                    rto_in_secs=123
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "rpo_in_secs": rpo_in_secs,
                "rto_in_secs": rto_in_secs,
            }

        @builtins.property
        def rpo_in_secs(self) -> jsii.Number:
            '''``CfnResiliencyPolicy.FailurePolicyProperty.RpoInSecs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html#cfn-resiliencehub-resiliencypolicy-failurepolicy-rpoinsecs
            '''
            result = self._values.get("rpo_in_secs")
            assert result is not None, "Required property 'rpo_in_secs' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def rto_in_secs(self) -> jsii.Number:
            '''``CfnResiliencyPolicy.FailurePolicyProperty.RtoInSecs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html#cfn-resiliencehub-resiliencypolicy-failurepolicy-rtoinsecs
            '''
            result = self._values.get("rto_in_secs")
            assert result is not None, "Required property 'rto_in_secs' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailurePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-resiliencehub.CfnResiliencyPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_location_constraint": "dataLocationConstraint",
        "policy": "policy",
        "policy_description": "policyDescription",
        "policy_name": "policyName",
        "tags": "tags",
        "tier": "tier",
    },
)
class CfnResiliencyPolicyProps:
    def __init__(
        self,
        *,
        data_location_constraint: typing.Optional[builtins.str] = None,
        policy: typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnResiliencyPolicy.FailurePolicyProperty]], aws_cdk.core.IResolvable],
        policy_description: typing.Optional[builtins.str] = None,
        policy_name: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tier: builtins.str,
    ) -> None:
        '''Properties for defining a ``AWS::ResilienceHub::ResiliencyPolicy``.

        :param data_location_constraint: ``AWS::ResilienceHub::ResiliencyPolicy.DataLocationConstraint``.
        :param policy: ``AWS::ResilienceHub::ResiliencyPolicy.Policy``.
        :param policy_description: ``AWS::ResilienceHub::ResiliencyPolicy.PolicyDescription``.
        :param policy_name: ``AWS::ResilienceHub::ResiliencyPolicy.PolicyName``.
        :param tags: ``AWS::ResilienceHub::ResiliencyPolicy.Tags``.
        :param tier: ``AWS::ResilienceHub::ResiliencyPolicy.Tier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_resiliencehub as resiliencehub
            
            cfn_resiliency_policy_props = resiliencehub.CfnResiliencyPolicyProps(
                policy={
                    "policy_key": resiliencehub.CfnResiliencyPolicy.FailurePolicyProperty(
                        rpo_in_secs=123,
                        rto_in_secs=123
                    )
                },
                policy_name="policyName",
                tier="tier",
            
                # the properties below are optional
                data_location_constraint="dataLocationConstraint",
                policy_description="policyDescription",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "policy": policy,
            "policy_name": policy_name,
            "tier": tier,
        }
        if data_location_constraint is not None:
            self._values["data_location_constraint"] = data_location_constraint
        if policy_description is not None:
            self._values["policy_description"] = policy_description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_location_constraint(self) -> typing.Optional[builtins.str]:
        '''``AWS::ResilienceHub::ResiliencyPolicy.DataLocationConstraint``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-datalocationconstraint
        '''
        result = self._values.get("data_location_constraint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(
        self,
    ) -> typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnResiliencyPolicy.FailurePolicyProperty]], aws_cdk.core.IResolvable]:
        '''``AWS::ResilienceHub::ResiliencyPolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnResiliencyPolicy.FailurePolicyProperty]], aws_cdk.core.IResolvable], result)

    @builtins.property
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::ResilienceHub::ResiliencyPolicy.PolicyDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policydescription
        '''
        result = self._values.get("policy_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''``AWS::ResilienceHub::ResiliencyPolicy.PolicyName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::ResilienceHub::ResiliencyPolicy.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tier(self) -> builtins.str:
        '''``AWS::ResilienceHub::ResiliencyPolicy.Tier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tier
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResiliencyPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApp",
    "CfnAppProps",
    "CfnResiliencyPolicy",
    "CfnResiliencyPolicyProps",
]

publication.publish()
