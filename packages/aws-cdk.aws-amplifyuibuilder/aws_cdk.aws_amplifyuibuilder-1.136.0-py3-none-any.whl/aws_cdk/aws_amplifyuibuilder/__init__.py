'''
# AWS::AmplifyUIBuilder Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AmplifyUIBuilder](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AmplifyUIBuilder.html).

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
class CfnComponent(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent",
):
    '''A CloudFormation ``AWS::AmplifyUIBuilder::Component``.

    :cloudformationResource: AWS::AmplifyUIBuilder::Component
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
        
        # component_child_property_ is of type ComponentChildProperty
        # component_property_property_ is of type ComponentPropertyProperty
        # predicate_property_ is of type PredicateProperty
        
        cfn_component = amplifyuibuilder.CfnComponent(self, "MyCfnComponent",
            binding_properties={
                "binding_properties_key": amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                        bucket="bucket",
                        default_value="defaultValue",
                        field="field",
                        key="key",
                        model="model",
                        predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                            and=[predicate_property_],
                            field="field",
                            operand="operand",
                            operator="operator",
                            or=[predicate_property_]
                        )],
                        user_attribute="userAttribute"
                    ),
                    default_value="defaultValue",
                    type="type"
                )
            },
            children=[amplifyuibuilder.CfnComponent.ComponentChildProperty(
                component_type="componentType",
                name="name",
                properties=amplifyuibuilder.CfnComponent.ComponentPropertiesProperty(),
        
                # the properties below are optional
                children=[component_child_property_]
            )],
            collection_properties={
                "collection_properties_key": amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty(
                    model="model",
        
                    # the properties below are optional
                    identifiers=["identifiers"],
                    predicate=amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    ),
                    sort=[amplifyuibuilder.CfnComponent.SortPropertyProperty(
                        direction="direction",
                        field="field"
                    )]
                )
            },
            component_type="componentType",
            name="name",
            overrides={
                "overrides_key": amplifyuibuilder.CfnComponent.ComponentOverridesValueProperty()
            },
            properties={
                "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
        
                        # the properties below are optional
                        field="field"
                    ),
                    bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
        
                        # the properties below are optional
                        field="field"
                    ),
                    concat=[component_property_property_],
                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                        else=component_property_property_,
                        field="field",
                        operand="operand",
                        operator="operator",
                        property="property",
                        then=component_property_property_
                    ),
                    configured=False,
                    default_value="defaultValue",
                    event="event",
                    imported_value="importedValue",
                    model="model",
                    type="type",
                    user_attribute="userAttribute",
                    value="value"
                )
            },
            source_id="sourceId",
            tags={
                "tags_key": "tags"
            },
            variants=[amplifyuibuilder.CfnComponent.ComponentVariantProperty(
                overrides=amplifyuibuilder.CfnComponent.ComponentOverridesProperty(),
                variant_values=amplifyuibuilder.CfnComponent.ComponentVariantValuesProperty()
            )]
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        binding_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentBindingPropertiesValueProperty"]], aws_cdk.core.IResolvable]] = None,
        children: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentChildProperty"]]]] = None,
        collection_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentDataConfigurationProperty"]]]] = None,
        component_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentOverridesValueProperty"]]]] = None,
        properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]]] = None,
        source_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variants: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentVariantProperty"]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AmplifyUIBuilder::Component``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param binding_properties: ``AWS::AmplifyUIBuilder::Component.BindingProperties``.
        :param children: ``AWS::AmplifyUIBuilder::Component.Children``.
        :param collection_properties: ``AWS::AmplifyUIBuilder::Component.CollectionProperties``.
        :param component_type: ``AWS::AmplifyUIBuilder::Component.ComponentType``.
        :param name: ``AWS::AmplifyUIBuilder::Component.Name``.
        :param overrides: ``AWS::AmplifyUIBuilder::Component.Overrides``.
        :param properties: ``AWS::AmplifyUIBuilder::Component.Properties``.
        :param source_id: ``AWS::AmplifyUIBuilder::Component.SourceId``.
        :param tags: ``AWS::AmplifyUIBuilder::Component.Tags``.
        :param variants: ``AWS::AmplifyUIBuilder::Component.Variants``.
        '''
        props = CfnComponentProps(
            binding_properties=binding_properties,
            children=children,
            collection_properties=collection_properties,
            component_type=component_type,
            name=name,
            overrides=overrides,
            properties=properties,
            source_id=source_id,
            tags=tags,
            variants=variants,
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
    @jsii.member(jsii_name="attrAppId")
    def attr_app_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: AppId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrEnvironmentName")
    def attr_environment_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: EnvironmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrModifiedAt")
    def attr_modified_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: ModifiedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedAt"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bindingProperties")
    def binding_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentBindingPropertiesValueProperty"]]]]:
        '''``AWS::AmplifyUIBuilder::Component.BindingProperties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-bindingproperties
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentBindingPropertiesValueProperty"]]]], jsii.get(self, "bindingProperties"))

    @binding_properties.setter
    def binding_properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentBindingPropertiesValueProperty"]]]],
    ) -> None:
        jsii.set(self, "bindingProperties", value)

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
    @jsii.member(jsii_name="children")
    def children(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentChildProperty"]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Children``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-children
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentChildProperty"]]]], jsii.get(self, "children"))

    @children.setter
    def children(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentChildProperty"]]]],
    ) -> None:
        jsii.set(self, "children", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="collectionProperties")
    def collection_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentDataConfigurationProperty"]]]]:
        '''``AWS::AmplifyUIBuilder::Component.CollectionProperties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-collectionproperties
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentDataConfigurationProperty"]]]], jsii.get(self, "collectionProperties"))

    @collection_properties.setter
    def collection_properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentDataConfigurationProperty"]]]],
    ) -> None:
        jsii.set(self, "collectionProperties", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="componentType")
    def component_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::AmplifyUIBuilder::Component.ComponentType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-componenttype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentType"))

    @component_type.setter
    def component_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "componentType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AmplifyUIBuilder::Component.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="overrides")
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentOverridesValueProperty"]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Overrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-overrides
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentOverridesValueProperty"]]]], jsii.get(self, "overrides"))

    @overrides.setter
    def overrides(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentOverridesValueProperty"]]]],
    ) -> None:
        jsii.set(self, "overrides", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Properties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-properties
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]]], jsii.get(self, "properties"))

    @properties.setter
    def properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]]],
    ) -> None:
        jsii.set(self, "properties", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::AmplifyUIBuilder::Component.SourceId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-sourceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sourceId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AmplifyUIBuilder::Component.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variants")
    def variants(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentVariantProperty"]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Variants``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-variants
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentVariantProperty"]]]], jsii.get(self, "variants"))

    @variants.setter
    def variants(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentVariantProperty"]]]],
    ) -> None:
        jsii.set(self, "variants", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "default_value": "defaultValue",
            "field": "field",
            "key": "key",
            "model": "model",
            "predicates": "predicates",
            "user_attribute": "userAttribute",
        },
    )
    class ComponentBindingPropertiesValuePropertiesProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            field: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            model: typing.Optional[builtins.str] = None,
            predicates: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]] = None,
            user_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket: ``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Bucket``.
            :param default_value: ``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.DefaultValue``.
            :param field: ``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Field``.
            :param key: ``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Key``.
            :param model: ``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Model``.
            :param predicates: ``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Predicates``.
            :param user_attribute: ``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.UserAttribute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_ is of type PredicateProperty
                
                component_binding_properties_value_properties_property = amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                    bucket="bucket",
                    default_value="defaultValue",
                    field="field",
                    key="key",
                    model="model",
                    predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    )],
                    user_attribute="userAttribute"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if default_value is not None:
                self._values["default_value"] = default_value
            if field is not None:
                self._values["field"] = field
            if key is not None:
                self._values["key"] = key
            if model is not None:
                self._values["model"] = model
            if predicates is not None:
                self._values["predicates"] = predicates
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Field``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Model``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def predicates(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]]:
            '''``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.Predicates``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-predicates
            '''
            result = self._values.get("predicates")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValuePropertiesProperty.UserAttribute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentBindingPropertiesValuePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binding_properties": "bindingProperties",
            "default_value": "defaultValue",
            "type": "type",
        },
    )
    class ComponentBindingPropertiesValueProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentBindingPropertiesValuePropertiesProperty"]] = None,
            default_value: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param binding_properties: ``CfnComponent.ComponentBindingPropertiesValueProperty.BindingProperties``.
            :param default_value: ``CfnComponent.ComponentBindingPropertiesValueProperty.DefaultValue``.
            :param type: ``CfnComponent.ComponentBindingPropertiesValueProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_ is of type PredicateProperty
                
                component_binding_properties_value_property = amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                        bucket="bucket",
                        default_value="defaultValue",
                        field="field",
                        key="key",
                        model="model",
                        predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                            and=[predicate_property_],
                            field="field",
                            operand="operand",
                            operator="operator",
                            or=[predicate_property_]
                        )],
                        user_attribute="userAttribute"
                    ),
                    default_value="defaultValue",
                    type="type"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if default_value is not None:
                self._values["default_value"] = default_value
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentBindingPropertiesValuePropertiesProperty"]]:
            '''``CfnComponent.ComponentBindingPropertiesValueProperty.BindingProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentBindingPropertiesValuePropertiesProperty"]], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValueProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentBindingPropertiesValueProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentBindingPropertiesValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentChildProperty",
        jsii_struct_bases=[],
        name_mapping={
            "children": "children",
            "component_type": "componentType",
            "name": "name",
            "properties": "properties",
        },
    )
    class ComponentChildProperty:
        def __init__(
            self,
            *,
            children: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentChildProperty"]]]] = None,
            component_type: builtins.str,
            name: builtins.str,
            properties: typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertiesProperty"],
        ) -> None:
            '''
            :param children: ``CfnComponent.ComponentChildProperty.Children``.
            :param component_type: ``CfnComponent.ComponentChildProperty.ComponentType``.
            :param name: ``CfnComponent.ComponentChildProperty.Name``.
            :param properties: ``CfnComponent.ComponentChildProperty.Properties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # component_child_property_ is of type ComponentChildProperty
                
                component_child_property = amplifyuibuilder.CfnComponent.ComponentChildProperty(
                    component_type="componentType",
                    name="name",
                    properties=amplifyuibuilder.CfnComponent.ComponentPropertiesProperty(),
                
                    # the properties below are optional
                    children=[amplifyuibuilder.CfnComponent.ComponentChildProperty(
                        component_type="componentType",
                        name="name",
                        properties=amplifyuibuilder.CfnComponent.ComponentPropertiesProperty(),
                
                        # the properties below are optional
                        children=[component_child_property_]
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "component_type": component_type,
                "name": name,
                "properties": properties,
            }
            if children is not None:
                self._values["children"] = children

        @builtins.property
        def children(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentChildProperty"]]]]:
            '''``CfnComponent.ComponentChildProperty.Children``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentChildProperty"]]]], result)

        @builtins.property
        def component_type(self) -> builtins.str:
            '''``CfnComponent.ComponentChildProperty.ComponentType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-componenttype
            '''
            result = self._values.get("component_type")
            assert result is not None, "Required property 'component_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnComponent.ComponentChildProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertiesProperty"]:
            '''``CfnComponent.ComponentChildProperty.Properties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-properties
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertiesProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentChildProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "else_": "else",
            "field": "field",
            "operand": "operand",
            "operator": "operator",
            "property": "property",
            "then": "then",
        },
    )
    class ComponentConditionPropertyProperty:
        def __init__(
            self,
            *,
            else_: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]] = None,
            field: typing.Optional[builtins.str] = None,
            operand: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
            then: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]] = None,
        ) -> None:
            '''
            :param else_: ``CfnComponent.ComponentConditionPropertyProperty.Else``.
            :param field: ``CfnComponent.ComponentConditionPropertyProperty.Field``.
            :param operand: ``CfnComponent.ComponentConditionPropertyProperty.Operand``.
            :param operator: ``CfnComponent.ComponentConditionPropertyProperty.Operator``.
            :param property: ``CfnComponent.ComponentConditionPropertyProperty.Property``.
            :param then: ``CfnComponent.ComponentConditionPropertyProperty.Then``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # component_property_property_ is of type ComponentPropertyProperty
                
                component_condition_property_property = amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                    else=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    field="field",
                    operand="operand",
                    operator="operator",
                    property="property",
                    then=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if else_ is not None:
                self._values["else_"] = else_
            if field is not None:
                self._values["field"] = field
            if operand is not None:
                self._values["operand"] = operand
            if operator is not None:
                self._values["operator"] = operator
            if property is not None:
                self._values["property"] = property
            if then is not None:
                self._values["then"] = then

        @builtins.property
        def else_(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]:
            '''``CfnComponent.ComponentConditionPropertyProperty.Else``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-else
            '''
            result = self._values.get("else_")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentConditionPropertyProperty.Field``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentConditionPropertyProperty.Operand``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operand
            '''
            result = self._values.get("operand")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentConditionPropertyProperty.Operator``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentConditionPropertyProperty.Property``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def then(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]:
            '''``CfnComponent.ComponentConditionPropertyProperty.Then``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-then
            '''
            result = self._values.get("then")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConditionPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "identifiers": "identifiers",
            "model": "model",
            "predicate": "predicate",
            "sort": "sort",
        },
    )
    class ComponentDataConfigurationProperty:
        def __init__(
            self,
            *,
            identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
            model: builtins.str,
            predicate: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]] = None,
            sort: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.SortPropertyProperty"]]]] = None,
        ) -> None:
            '''
            :param identifiers: ``CfnComponent.ComponentDataConfigurationProperty.Identifiers``.
            :param model: ``CfnComponent.ComponentDataConfigurationProperty.Model``.
            :param predicate: ``CfnComponent.ComponentDataConfigurationProperty.Predicate``.
            :param sort: ``CfnComponent.ComponentDataConfigurationProperty.Sort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_ is of type PredicateProperty
                
                component_data_configuration_property = amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty(
                    model="model",
                
                    # the properties below are optional
                    identifiers=["identifiers"],
                    predicate=amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    ),
                    sort=[amplifyuibuilder.CfnComponent.SortPropertyProperty(
                        direction="direction",
                        field="field"
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "model": model,
            }
            if identifiers is not None:
                self._values["identifiers"] = identifiers
            if predicate is not None:
                self._values["predicate"] = predicate
            if sort is not None:
                self._values["sort"] = sort

        @builtins.property
        def identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnComponent.ComponentDataConfigurationProperty.Identifiers``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-identifiers
            '''
            result = self._values.get("identifiers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def model(self) -> builtins.str:
            '''``CfnComponent.ComponentDataConfigurationProperty.Model``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-model
            '''
            result = self._values.get("model")
            assert result is not None, "Required property 'model' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def predicate(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]:
            '''``CfnComponent.ComponentDataConfigurationProperty.Predicate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-predicate
            '''
            result = self._values.get("predicate")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]], result)

        @builtins.property
        def sort(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.SortPropertyProperty"]]]]:
            '''``CfnComponent.ComponentDataConfigurationProperty.Sort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-sort
            '''
            result = self._values.get("sort")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.SortPropertyProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentDataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class ComponentOverridesProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentoverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                component_overrides_property = amplifyuibuilder.CfnComponent.ComponentOverridesProperty()
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentOverridesValueProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class ComponentOverridesValueProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentoverridesvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                component_overrides_value_property = amplifyuibuilder.CfnComponent.ComponentOverridesValueProperty()
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentOverridesValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class ComponentPropertiesProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                component_properties_property = amplifyuibuilder.CfnComponent.ComponentPropertiesProperty()
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"field": "field", "property": "property"},
    )
    class ComponentPropertyBindingPropertiesProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            property: builtins.str,
        ) -> None:
            '''
            :param field: ``CfnComponent.ComponentPropertyBindingPropertiesProperty.Field``.
            :param property: ``CfnComponent.ComponentPropertyBindingPropertiesProperty.Property``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                component_property_binding_properties_property = amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                    property="property",
                
                    # the properties below are optional
                    field="field"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "property": property,
            }
            if field is not None:
                self._values["field"] = field

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyBindingPropertiesProperty.Field``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html#cfn-amplifyuibuilder-component-componentpropertybindingproperties-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> builtins.str:
            '''``CfnComponent.ComponentPropertyBindingPropertiesProperty.Property``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html#cfn-amplifyuibuilder-component-componentpropertybindingproperties-property
            '''
            result = self._values.get("property")
            assert result is not None, "Required property 'property' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPropertyBindingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binding_properties": "bindingProperties",
            "bindings": "bindings",
            "collection_binding_properties": "collectionBindingProperties",
            "concat": "concat",
            "condition": "condition",
            "configured": "configured",
            "default_value": "defaultValue",
            "event": "event",
            "imported_value": "importedValue",
            "model": "model",
            "type": "type",
            "user_attribute": "userAttribute",
            "value": "value",
        },
    )
    class ComponentPropertyProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyBindingPropertiesProperty"]] = None,
            bindings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.FormBindingsProperty"]] = None,
            collection_binding_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyBindingPropertiesProperty"]] = None,
            concat: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]]] = None,
            condition: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentConditionPropertyProperty"]] = None,
            configured: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            default_value: typing.Optional[builtins.str] = None,
            event: typing.Optional[builtins.str] = None,
            imported_value: typing.Optional[builtins.str] = None,
            model: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            user_attribute: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param binding_properties: ``CfnComponent.ComponentPropertyProperty.BindingProperties``.
            :param bindings: ``CfnComponent.ComponentPropertyProperty.Bindings``.
            :param collection_binding_properties: ``CfnComponent.ComponentPropertyProperty.CollectionBindingProperties``.
            :param concat: ``CfnComponent.ComponentPropertyProperty.Concat``.
            :param condition: ``CfnComponent.ComponentPropertyProperty.Condition``.
            :param configured: ``CfnComponent.ComponentPropertyProperty.Configured``.
            :param default_value: ``CfnComponent.ComponentPropertyProperty.DefaultValue``.
            :param event: ``CfnComponent.ComponentPropertyProperty.Event``.
            :param imported_value: ``CfnComponent.ComponentPropertyProperty.ImportedValue``.
            :param model: ``CfnComponent.ComponentPropertyProperty.Model``.
            :param type: ``CfnComponent.ComponentPropertyProperty.Type``.
            :param user_attribute: ``CfnComponent.ComponentPropertyProperty.UserAttribute``.
            :param value: ``CfnComponent.ComponentPropertyProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # component_condition_property_property_ is of type ComponentConditionPropertyProperty
                # component_property_property_ is of type ComponentPropertyProperty
                
                component_property_property = amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
                
                        # the properties below are optional
                        field="field"
                    ),
                    bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
                
                        # the properties below are optional
                        field="field"
                    ),
                    concat=[amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )],
                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                        else=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            concat=[component_property_property_],
                            condition=component_condition_property_property_,
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        field="field",
                        operand="operand",
                        operator="operator",
                        property="property",
                        then=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            concat=[component_property_property_],
                            condition=component_condition_property_property_,
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    ),
                    configured=False,
                    default_value="defaultValue",
                    event="event",
                    imported_value="importedValue",
                    model="model",
                    type="type",
                    user_attribute="userAttribute",
                    value="value"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if bindings is not None:
                self._values["bindings"] = bindings
            if collection_binding_properties is not None:
                self._values["collection_binding_properties"] = collection_binding_properties
            if concat is not None:
                self._values["concat"] = concat
            if condition is not None:
                self._values["condition"] = condition
            if configured is not None:
                self._values["configured"] = configured
            if default_value is not None:
                self._values["default_value"] = default_value
            if event is not None:
                self._values["event"] = event
            if imported_value is not None:
                self._values["imported_value"] = imported_value
            if model is not None:
                self._values["model"] = model
            if type is not None:
                self._values["type"] = type
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyBindingPropertiesProperty"]]:
            '''``CfnComponent.ComponentPropertyProperty.BindingProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyBindingPropertiesProperty"]], result)

        @builtins.property
        def bindings(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.FormBindingsProperty"]]:
            '''``CfnComponent.ComponentPropertyProperty.Bindings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-bindings
            '''
            result = self._values.get("bindings")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.FormBindingsProperty"]], result)

        @builtins.property
        def collection_binding_properties(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyBindingPropertiesProperty"]]:
            '''``CfnComponent.ComponentPropertyProperty.CollectionBindingProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-collectionbindingproperties
            '''
            result = self._values.get("collection_binding_properties")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyBindingPropertiesProperty"]], result)

        @builtins.property
        def concat(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]]]:
            '''``CfnComponent.ComponentPropertyProperty.Concat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-concat
            '''
            result = self._values.get("concat")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentPropertyProperty"]]]], result)

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentConditionPropertyProperty"]]:
            '''``CfnComponent.ComponentPropertyProperty.Condition``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentConditionPropertyProperty"]], result)

        @builtins.property
        def configured(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnComponent.ComponentPropertyProperty.Configured``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-configured
            '''
            result = self._values.get("configured")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyProperty.Event``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-event
            '''
            result = self._values.get("event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def imported_value(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyProperty.ImportedValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-importedvalue
            '''
            result = self._values.get("imported_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyProperty.Model``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyProperty.UserAttribute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.ComponentPropertyProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentVariantProperty",
        jsii_struct_bases=[],
        name_mapping={"overrides": "overrides", "variant_values": "variantValues"},
    )
    class ComponentVariantProperty:
        def __init__(
            self,
            *,
            overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentOverridesProperty"]] = None,
            variant_values: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentVariantValuesProperty"]] = None,
        ) -> None:
            '''
            :param overrides: ``CfnComponent.ComponentVariantProperty.Overrides``.
            :param variant_values: ``CfnComponent.ComponentVariantProperty.VariantValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                component_variant_property = amplifyuibuilder.CfnComponent.ComponentVariantProperty(
                    overrides=amplifyuibuilder.CfnComponent.ComponentOverridesProperty(),
                    variant_values=amplifyuibuilder.CfnComponent.ComponentVariantValuesProperty()
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if overrides is not None:
                self._values["overrides"] = overrides
            if variant_values is not None:
                self._values["variant_values"] = variant_values

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentOverridesProperty"]]:
            '''``CfnComponent.ComponentVariantProperty.Overrides``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html#cfn-amplifyuibuilder-component-componentvariant-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentOverridesProperty"]], result)

        @builtins.property
        def variant_values(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentVariantValuesProperty"]]:
            '''``CfnComponent.ComponentVariantProperty.VariantValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html#cfn-amplifyuibuilder-component-componentvariant-variantvalues
            '''
            result = self._values.get("variant_values")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.ComponentVariantValuesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentVariantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.ComponentVariantValuesProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class ComponentVariantValuesProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariantvalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                component_variant_values_property = amplifyuibuilder.CfnComponent.ComponentVariantValuesProperty()
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentVariantValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.FormBindingsProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class FormBindingsProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-formbindings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                form_bindings_property = amplifyuibuilder.CfnComponent.FormBindingsProperty()
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormBindingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_": "and",
            "field": "field",
            "operand": "operand",
            "operator": "operator",
            "or_": "or",
        },
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            and_: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]] = None,
            field: typing.Optional[builtins.str] = None,
            operand: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            or_: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]] = None,
        ) -> None:
            '''
            :param and_: ``CfnComponent.PredicateProperty.And``.
            :param field: ``CfnComponent.PredicateProperty.Field``.
            :param operand: ``CfnComponent.PredicateProperty.Operand``.
            :param operator: ``CfnComponent.PredicateProperty.Operator``.
            :param or_: ``CfnComponent.PredicateProperty.Or``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_ is of type PredicateProperty
                
                predicate_property = amplifyuibuilder.CfnComponent.PredicateProperty(
                    and=[amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    )],
                    field="field",
                    operand="operand",
                    operator="operator",
                    or=[amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if and_ is not None:
                self._values["and_"] = and_
            if field is not None:
                self._values["field"] = field
            if operand is not None:
                self._values["operand"] = operand
            if operator is not None:
                self._values["operator"] = operator
            if or_ is not None:
                self._values["or_"] = or_

        @builtins.property
        def and_(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]]:
            '''``CfnComponent.PredicateProperty.And``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-and
            '''
            result = self._values.get("and_")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.PredicateProperty.Field``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.PredicateProperty.Operand``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-operand
            '''
            result = self._values.get("operand")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''``CfnComponent.PredicateProperty.Operator``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def or_(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]]:
            '''``CfnComponent.PredicateProperty.Or``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-or
            '''
            result = self._values.get("or_")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnComponent.PredicateProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredicateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponent.SortPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"direction": "direction", "field": "field"},
    )
    class SortPropertyProperty:
        def __init__(self, *, direction: builtins.str, field: builtins.str) -> None:
            '''
            :param direction: ``CfnComponent.SortPropertyProperty.Direction``.
            :param field: ``CfnComponent.SortPropertyProperty.Field``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                sort_property_property = amplifyuibuilder.CfnComponent.SortPropertyProperty(
                    direction="direction",
                    field="field"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "direction": direction,
                "field": field,
            }

        @builtins.property
        def direction(self) -> builtins.str:
            '''``CfnComponent.SortPropertyProperty.Direction``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html#cfn-amplifyuibuilder-component-sortproperty-direction
            '''
            result = self._values.get("direction")
            assert result is not None, "Required property 'direction' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field(self) -> builtins.str:
            '''``CfnComponent.SortPropertyProperty.Field``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html#cfn-amplifyuibuilder-component-sortproperty-field
            '''
            result = self._values.get("field")
            assert result is not None, "Required property 'field' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SortPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "binding_properties": "bindingProperties",
        "children": "children",
        "collection_properties": "collectionProperties",
        "component_type": "componentType",
        "name": "name",
        "overrides": "overrides",
        "properties": "properties",
        "source_id": "sourceId",
        "tags": "tags",
        "variants": "variants",
    },
)
class CfnComponentProps:
    def __init__(
        self,
        *,
        binding_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentBindingPropertiesValueProperty]], aws_cdk.core.IResolvable]] = None,
        children: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentChildProperty]]]] = None,
        collection_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentDataConfigurationProperty]]]] = None,
        component_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentOverridesValueProperty]]]] = None,
        properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentPropertyProperty]]]] = None,
        source_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        variants: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentVariantProperty]]]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AmplifyUIBuilder::Component``.

        :param binding_properties: ``AWS::AmplifyUIBuilder::Component.BindingProperties``.
        :param children: ``AWS::AmplifyUIBuilder::Component.Children``.
        :param collection_properties: ``AWS::AmplifyUIBuilder::Component.CollectionProperties``.
        :param component_type: ``AWS::AmplifyUIBuilder::Component.ComponentType``.
        :param name: ``AWS::AmplifyUIBuilder::Component.Name``.
        :param overrides: ``AWS::AmplifyUIBuilder::Component.Overrides``.
        :param properties: ``AWS::AmplifyUIBuilder::Component.Properties``.
        :param source_id: ``AWS::AmplifyUIBuilder::Component.SourceId``.
        :param tags: ``AWS::AmplifyUIBuilder::Component.Tags``.
        :param variants: ``AWS::AmplifyUIBuilder::Component.Variants``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
            
            # component_child_property_ is of type ComponentChildProperty
            # component_property_property_ is of type ComponentPropertyProperty
            # predicate_property_ is of type PredicateProperty
            
            cfn_component_props = amplifyuibuilder.CfnComponentProps(
                binding_properties={
                    "binding_properties_key": amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                            bucket="bucket",
                            default_value="defaultValue",
                            field="field",
                            key="key",
                            model="model",
                            predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                                and=[predicate_property_],
                                field="field",
                                operand="operand",
                                operator="operator",
                                or=[predicate_property_]
                            )],
                            user_attribute="userAttribute"
                        ),
                        default_value="defaultValue",
                        type="type"
                    )
                },
                children=[amplifyuibuilder.CfnComponent.ComponentChildProperty(
                    component_type="componentType",
                    name="name",
                    properties=amplifyuibuilder.CfnComponent.ComponentPropertiesProperty(),
            
                    # the properties below are optional
                    children=[component_child_property_]
                )],
                collection_properties={
                    "collection_properties_key": amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty(
                        model="model",
            
                        # the properties below are optional
                        identifiers=["identifiers"],
                        predicate=amplifyuibuilder.CfnComponent.PredicateProperty(
                            and=[predicate_property_],
                            field="field",
                            operand="operand",
                            operator="operator",
                            or=[predicate_property_]
                        ),
                        sort=[amplifyuibuilder.CfnComponent.SortPropertyProperty(
                            direction="direction",
                            field="field"
                        )]
                    )
                },
                component_type="componentType",
                name="name",
                overrides={
                    "overrides_key": amplifyuibuilder.CfnComponent.ComponentOverridesValueProperty()
                },
                properties={
                    "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
            
                            # the properties below are optional
                            field="field"
                        ),
                        bindings=amplifyuibuilder.CfnComponent.FormBindingsProperty(),
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
            
                            # the properties below are optional
                            field="field"
                        ),
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                },
                source_id="sourceId",
                tags={
                    "tags_key": "tags"
                },
                variants=[amplifyuibuilder.CfnComponent.ComponentVariantProperty(
                    overrides=amplifyuibuilder.CfnComponent.ComponentOverridesProperty(),
                    variant_values=amplifyuibuilder.CfnComponent.ComponentVariantValuesProperty()
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if binding_properties is not None:
            self._values["binding_properties"] = binding_properties
        if children is not None:
            self._values["children"] = children
        if collection_properties is not None:
            self._values["collection_properties"] = collection_properties
        if component_type is not None:
            self._values["component_type"] = component_type
        if name is not None:
            self._values["name"] = name
        if overrides is not None:
            self._values["overrides"] = overrides
        if properties is not None:
            self._values["properties"] = properties
        if source_id is not None:
            self._values["source_id"] = source_id
        if tags is not None:
            self._values["tags"] = tags
        if variants is not None:
            self._values["variants"] = variants

    @builtins.property
    def binding_properties(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentBindingPropertiesValueProperty]], aws_cdk.core.IResolvable]]:
        '''``AWS::AmplifyUIBuilder::Component.BindingProperties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-bindingproperties
        '''
        result = self._values.get("binding_properties")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentBindingPropertiesValueProperty]], aws_cdk.core.IResolvable]], result)

    @builtins.property
    def children(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentChildProperty]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Children``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-children
        '''
        result = self._values.get("children")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentChildProperty]]]], result)

    @builtins.property
    def collection_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentDataConfigurationProperty]]]]:
        '''``AWS::AmplifyUIBuilder::Component.CollectionProperties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-collectionproperties
        '''
        result = self._values.get("collection_properties")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentDataConfigurationProperty]]]], result)

    @builtins.property
    def component_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::AmplifyUIBuilder::Component.ComponentType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-componenttype
        '''
        result = self._values.get("component_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AmplifyUIBuilder::Component.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentOverridesValueProperty]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Overrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-overrides
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentOverridesValueProperty]]]], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentPropertyProperty]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Properties``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentPropertyProperty]]]], result)

    @builtins.property
    def source_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::AmplifyUIBuilder::Component.SourceId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-sourceid
        '''
        result = self._values.get("source_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::AmplifyUIBuilder::Component.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def variants(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentVariantProperty]]]]:
        '''``AWS::AmplifyUIBuilder::Component.Variants``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-variants
        '''
        result = self._values.get("variants")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnComponent.ComponentVariantProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTheme(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnTheme",
):
    '''A CloudFormation ``AWS::AmplifyUIBuilder::Theme``.

    :cloudformationResource: AWS::AmplifyUIBuilder::Theme
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
        
        # theme_values_property_ is of type ThemeValuesProperty
        
        cfn_theme = amplifyuibuilder.CfnTheme(self, "MyCfnTheme",
            name="name",
            values=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                key="key",
                value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                    children=[theme_values_property_],
                    value="value"
                )
            )],
        
            # the properties below are optional
            overrides=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                key="key",
                value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                    children=[theme_values_property_],
                    value="value"
                )
            )],
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
        name: builtins.str,
        overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        values: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]],
    ) -> None:
        '''Create a new ``AWS::AmplifyUIBuilder::Theme``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::AmplifyUIBuilder::Theme.Name``.
        :param overrides: ``AWS::AmplifyUIBuilder::Theme.Overrides``.
        :param tags: ``AWS::AmplifyUIBuilder::Theme.Tags``.
        :param values: ``AWS::AmplifyUIBuilder::Theme.Values``.
        '''
        props = CfnThemeProps(name=name, overrides=overrides, tags=tags, values=values)

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
    @jsii.member(jsii_name="attrAppId")
    def attr_app_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: AppId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrEnvironmentName")
    def attr_environment_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: EnvironmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrModifiedAt")
    def attr_modified_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: ModifiedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedAt"))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::AmplifyUIBuilder::Theme.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="overrides")
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]]:
        '''``AWS::AmplifyUIBuilder::Theme.Overrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-overrides
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]], jsii.get(self, "overrides"))

    @overrides.setter
    def overrides(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]],
    ) -> None:
        jsii.set(self, "overrides", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AmplifyUIBuilder::Theme.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]:
        '''``AWS::AmplifyUIBuilder::Theme.Values``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-values
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]], jsii.get(self, "values"))

    @values.setter
    def values(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]],
    ) -> None:
        jsii.set(self, "values", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnTheme.ThemeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"children": "children", "value": "value"},
    )
    class ThemeValueProperty:
        def __init__(
            self,
            *,
            children: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param children: ``CfnTheme.ThemeValueProperty.Children``.
            :param value: ``CfnTheme.ThemeValueProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # theme_values_property_ is of type ThemeValuesProperty
                
                theme_value_property = amplifyuibuilder.CfnTheme.ThemeValueProperty(
                    children=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                        key="key",
                        value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                            children=[theme_values_property_],
                            value="value"
                        )
                    )],
                    value="value"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if children is not None:
                self._values["children"] = children
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def children(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]]:
            '''``CfnTheme.ThemeValueProperty.Children``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html#cfn-amplifyuibuilder-theme-themevalue-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValuesProperty"]]]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnTheme.ThemeValueProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html#cfn-amplifyuibuilder-theme-themevalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThemeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnTheme.ThemeValuesProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ThemeValuesProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValueProperty"]] = None,
        ) -> None:
            '''
            :param key: ``CfnTheme.ThemeValuesProperty.Key``.
            :param value: ``CfnTheme.ThemeValuesProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
                
                # theme_value_property_ is of type ThemeValueProperty
                
                theme_values_property = amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                        children=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                            key="key",
                            value=theme_value_property_
                        )],
                        value="value"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnTheme.ThemeValuesProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html#cfn-amplifyuibuilder-theme-themevalues-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValueProperty"]]:
            '''``CfnTheme.ThemeValuesProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html#cfn-amplifyuibuilder-theme-themevalues-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnTheme.ThemeValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThemeValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplifyuibuilder.CfnThemeProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "overrides": "overrides",
        "tags": "tags",
        "values": "values",
    },
)
class CfnThemeProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnTheme.ThemeValuesProperty]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        values: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnTheme.ThemeValuesProperty]]],
    ) -> None:
        '''Properties for defining a ``AWS::AmplifyUIBuilder::Theme``.

        :param name: ``AWS::AmplifyUIBuilder::Theme.Name``.
        :param overrides: ``AWS::AmplifyUIBuilder::Theme.Overrides``.
        :param tags: ``AWS::AmplifyUIBuilder::Theme.Tags``.
        :param values: ``AWS::AmplifyUIBuilder::Theme.Values``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplifyuibuilder as amplifyuibuilder
            
            # theme_values_property_ is of type ThemeValuesProperty
            
            cfn_theme_props = amplifyuibuilder.CfnThemeProps(
                name="name",
                values=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                        children=[theme_values_property_],
                        value="value"
                    )
                )],
            
                # the properties below are optional
                overrides=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                        children=[theme_values_property_],
                        value="value"
                    )
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "values": values,
        }
        if overrides is not None:
            self._values["overrides"] = overrides
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::AmplifyUIBuilder::Theme.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTheme.ThemeValuesProperty]]]]:
        '''``AWS::AmplifyUIBuilder::Theme.Overrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-overrides
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTheme.ThemeValuesProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::AmplifyUIBuilder::Theme.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTheme.ThemeValuesProperty]]]:
        '''``AWS::AmplifyUIBuilder::Theme.Values``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-values
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnTheme.ThemeValuesProperty]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnThemeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnComponent",
    "CfnComponentProps",
    "CfnTheme",
    "CfnThemeProps",
]

publication.publish()
