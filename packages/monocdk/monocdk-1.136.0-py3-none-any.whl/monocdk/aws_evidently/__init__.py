'''
# AWS::Evidently Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as evidently
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Evidently](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Evidently.html).

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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnExperiment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_evidently.CfnExperiment",
):
    '''A CloudFormation ``AWS::Evidently::Experiment``.

    :cloudformationResource: AWS::Evidently::Experiment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_evidently as evidently
        
        cfn_experiment = evidently.CfnExperiment(self, "MyCfnExperiment",
            metric_goals=[evidently.CfnExperiment.MetricGoalObjectProperty(
                desired_change="desiredChange",
                entity_id_key="entityIdKey",
                event_pattern="eventPattern",
                metric_name="metricName",
                value_key="valueKey",
        
                # the properties below are optional
                unit_label="unitLabel"
            )],
            name="name",
            online_ab_config=evidently.CfnExperiment.OnlineAbConfigObjectProperty(
                control_treatment_name="controlTreatmentName",
                treatment_weights=[evidently.CfnExperiment.TreatmentToWeightProperty(
                    split_weight=123,
                    treatment="treatment"
                )]
            ),
            project="project",
            treatments=[evidently.CfnExperiment.TreatmentObjectProperty(
                feature="feature",
                treatment_name="treatmentName",
                variation="variation",
        
                # the properties below are optional
                description="description"
            )],
        
            # the properties below are optional
            description="description",
            randomization_salt="randomizationSalt",
            sampling_rate=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        metric_goals: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnExperiment.MetricGoalObjectProperty", _IResolvable_a771d0ef]]],
        name: builtins.str,
        online_ab_config: typing.Union["CfnExperiment.OnlineAbConfigObjectProperty", _IResolvable_a771d0ef],
        project: builtins.str,
        randomization_salt: typing.Optional[builtins.str] = None,
        sampling_rate: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
        treatments: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnExperiment.TreatmentObjectProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        '''Create a new ``AWS::Evidently::Experiment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Evidently::Experiment.Description``.
        :param metric_goals: ``AWS::Evidently::Experiment.MetricGoals``.
        :param name: ``AWS::Evidently::Experiment.Name``.
        :param online_ab_config: ``AWS::Evidently::Experiment.OnlineAbConfig``.
        :param project: ``AWS::Evidently::Experiment.Project``.
        :param randomization_salt: ``AWS::Evidently::Experiment.RandomizationSalt``.
        :param sampling_rate: ``AWS::Evidently::Experiment.SamplingRate``.
        :param tags: ``AWS::Evidently::Experiment.Tags``.
        :param treatments: ``AWS::Evidently::Experiment.Treatments``.
        '''
        props = CfnExperimentProps(
            description=description,
            metric_goals=metric_goals,
            name=name,
            online_ab_config=online_ab_config,
            project=project,
            randomization_salt=randomization_salt,
            sampling_rate=sampling_rate,
            tags=tags,
            treatments=treatments,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
        '''``AWS::Evidently::Experiment.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metricGoals")
    def metric_goals(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.MetricGoalObjectProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Experiment.MetricGoals``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-metricgoals
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.MetricGoalObjectProperty", _IResolvable_a771d0ef]]], jsii.get(self, "metricGoals"))

    @metric_goals.setter
    def metric_goals(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.MetricGoalObjectProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "metricGoals", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Experiment.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="onlineAbConfig")
    def online_ab_config(
        self,
    ) -> typing.Union["CfnExperiment.OnlineAbConfigObjectProperty", _IResolvable_a771d0ef]:
        '''``AWS::Evidently::Experiment.OnlineAbConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-onlineabconfig
        '''
        return typing.cast(typing.Union["CfnExperiment.OnlineAbConfigObjectProperty", _IResolvable_a771d0ef], jsii.get(self, "onlineAbConfig"))

    @online_ab_config.setter
    def online_ab_config(
        self,
        value: typing.Union["CfnExperiment.OnlineAbConfigObjectProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "onlineAbConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        '''``AWS::Evidently::Experiment.Project``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-project
        '''
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        jsii.set(self, "project", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="randomizationSalt")
    def randomization_salt(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Experiment.RandomizationSalt``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-randomizationsalt
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "randomizationSalt"))

    @randomization_salt.setter
    def randomization_salt(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "randomizationSalt", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="samplingRate")
    def sampling_rate(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Evidently::Experiment.SamplingRate``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-samplingrate
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingRate"))

    @sampling_rate.setter
    def sampling_rate(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "samplingRate", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Evidently::Experiment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="treatments")
    def treatments(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.TreatmentObjectProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Experiment.Treatments``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-treatments
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.TreatmentObjectProperty", _IResolvable_a771d0ef]]], jsii.get(self, "treatments"))

    @treatments.setter
    def treatments(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.TreatmentObjectProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "treatments", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnExperiment.MetricGoalObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_change": "desiredChange",
            "entity_id_key": "entityIdKey",
            "event_pattern": "eventPattern",
            "metric_name": "metricName",
            "unit_label": "unitLabel",
            "value_key": "valueKey",
        },
    )
    class MetricGoalObjectProperty:
        def __init__(
            self,
            *,
            desired_change: builtins.str,
            entity_id_key: builtins.str,
            event_pattern: builtins.str,
            metric_name: builtins.str,
            unit_label: typing.Optional[builtins.str] = None,
            value_key: builtins.str,
        ) -> None:
            '''
            :param desired_change: ``CfnExperiment.MetricGoalObjectProperty.DesiredChange``.
            :param entity_id_key: ``CfnExperiment.MetricGoalObjectProperty.EntityIdKey``.
            :param event_pattern: ``CfnExperiment.MetricGoalObjectProperty.EventPattern``.
            :param metric_name: ``CfnExperiment.MetricGoalObjectProperty.MetricName``.
            :param unit_label: ``CfnExperiment.MetricGoalObjectProperty.UnitLabel``.
            :param value_key: ``CfnExperiment.MetricGoalObjectProperty.ValueKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                metric_goal_object_property = evidently.CfnExperiment.MetricGoalObjectProperty(
                    desired_change="desiredChange",
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    value_key="valueKey",
                
                    # the properties below are optional
                    unit_label="unitLabel"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "desired_change": desired_change,
                "entity_id_key": entity_id_key,
                "event_pattern": event_pattern,
                "metric_name": metric_name,
                "value_key": value_key,
            }
            if unit_label is not None:
                self._values["unit_label"] = unit_label

        @builtins.property
        def desired_change(self) -> builtins.str:
            '''``CfnExperiment.MetricGoalObjectProperty.DesiredChange``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-desiredchange
            '''
            result = self._values.get("desired_change")
            assert result is not None, "Required property 'desired_change' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def entity_id_key(self) -> builtins.str:
            '''``CfnExperiment.MetricGoalObjectProperty.EntityIdKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-entityidkey
            '''
            result = self._values.get("entity_id_key")
            assert result is not None, "Required property 'entity_id_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def event_pattern(self) -> builtins.str:
            '''``CfnExperiment.MetricGoalObjectProperty.EventPattern``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-eventpattern
            '''
            result = self._values.get("event_pattern")
            assert result is not None, "Required property 'event_pattern' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''``CfnExperiment.MetricGoalObjectProperty.MetricName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def unit_label(self) -> typing.Optional[builtins.str]:
            '''``CfnExperiment.MetricGoalObjectProperty.UnitLabel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-unitlabel
            '''
            result = self._values.get("unit_label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_key(self) -> builtins.str:
            '''``CfnExperiment.MetricGoalObjectProperty.ValueKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-metricgoalobject.html#cfn-evidently-experiment-metricgoalobject-valuekey
            '''
            result = self._values.get("value_key")
            assert result is not None, "Required property 'value_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricGoalObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnExperiment.OnlineAbConfigObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "control_treatment_name": "controlTreatmentName",
            "treatment_weights": "treatmentWeights",
        },
    )
    class OnlineAbConfigObjectProperty:
        def __init__(
            self,
            *,
            control_treatment_name: typing.Optional[builtins.str] = None,
            treatment_weights: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnExperiment.TreatmentToWeightProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param control_treatment_name: ``CfnExperiment.OnlineAbConfigObjectProperty.ControlTreatmentName``.
            :param treatment_weights: ``CfnExperiment.OnlineAbConfigObjectProperty.TreatmentWeights``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-onlineabconfigobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                online_ab_config_object_property = evidently.CfnExperiment.OnlineAbConfigObjectProperty(
                    control_treatment_name="controlTreatmentName",
                    treatment_weights=[evidently.CfnExperiment.TreatmentToWeightProperty(
                        split_weight=123,
                        treatment="treatment"
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if control_treatment_name is not None:
                self._values["control_treatment_name"] = control_treatment_name
            if treatment_weights is not None:
                self._values["treatment_weights"] = treatment_weights

        @builtins.property
        def control_treatment_name(self) -> typing.Optional[builtins.str]:
            '''``CfnExperiment.OnlineAbConfigObjectProperty.ControlTreatmentName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-onlineabconfigobject.html#cfn-evidently-experiment-onlineabconfigobject-controltreatmentname
            '''
            result = self._values.get("control_treatment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def treatment_weights(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.TreatmentToWeightProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnExperiment.OnlineAbConfigObjectProperty.TreatmentWeights``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-onlineabconfigobject.html#cfn-evidently-experiment-onlineabconfigobject-treatmentweights
            '''
            result = self._values.get("treatment_weights")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnExperiment.TreatmentToWeightProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnlineAbConfigObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnExperiment.TreatmentObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "feature": "feature",
            "treatment_name": "treatmentName",
            "variation": "variation",
        },
    )
    class TreatmentObjectProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            feature: builtins.str,
            treatment_name: builtins.str,
            variation: builtins.str,
        ) -> None:
            '''
            :param description: ``CfnExperiment.TreatmentObjectProperty.Description``.
            :param feature: ``CfnExperiment.TreatmentObjectProperty.Feature``.
            :param treatment_name: ``CfnExperiment.TreatmentObjectProperty.TreatmentName``.
            :param variation: ``CfnExperiment.TreatmentObjectProperty.Variation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                treatment_object_property = evidently.CfnExperiment.TreatmentObjectProperty(
                    feature="feature",
                    treatment_name="treatmentName",
                    variation="variation",
                
                    # the properties below are optional
                    description="description"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "feature": feature,
                "treatment_name": treatment_name,
                "variation": variation,
            }
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnExperiment.TreatmentObjectProperty.Description``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def feature(self) -> builtins.str:
            '''``CfnExperiment.TreatmentObjectProperty.Feature``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-feature
            '''
            result = self._values.get("feature")
            assert result is not None, "Required property 'feature' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def treatment_name(self) -> builtins.str:
            '''``CfnExperiment.TreatmentObjectProperty.TreatmentName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-treatmentname
            '''
            result = self._values.get("treatment_name")
            assert result is not None, "Required property 'treatment_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def variation(self) -> builtins.str:
            '''``CfnExperiment.TreatmentObjectProperty.Variation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmentobject.html#cfn-evidently-experiment-treatmentobject-variation
            '''
            result = self._values.get("variation")
            assert result is not None, "Required property 'variation' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TreatmentObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnExperiment.TreatmentToWeightProperty",
        jsii_struct_bases=[],
        name_mapping={"split_weight": "splitWeight", "treatment": "treatment"},
    )
    class TreatmentToWeightProperty:
        def __init__(
            self,
            *,
            split_weight: jsii.Number,
            treatment: builtins.str,
        ) -> None:
            '''
            :param split_weight: ``CfnExperiment.TreatmentToWeightProperty.SplitWeight``.
            :param treatment: ``CfnExperiment.TreatmentToWeightProperty.Treatment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmenttoweight.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                treatment_to_weight_property = evidently.CfnExperiment.TreatmentToWeightProperty(
                    split_weight=123,
                    treatment="treatment"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "split_weight": split_weight,
                "treatment": treatment,
            }

        @builtins.property
        def split_weight(self) -> jsii.Number:
            '''``CfnExperiment.TreatmentToWeightProperty.SplitWeight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmenttoweight.html#cfn-evidently-experiment-treatmenttoweight-splitweight
            '''
            result = self._values.get("split_weight")
            assert result is not None, "Required property 'split_weight' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def treatment(self) -> builtins.str:
            '''``CfnExperiment.TreatmentToWeightProperty.Treatment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-experiment-treatmenttoweight.html#cfn-evidently-experiment-treatmenttoweight-treatment
            '''
            result = self._values.get("treatment")
            assert result is not None, "Required property 'treatment' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TreatmentToWeightProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_evidently.CfnExperimentProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "metric_goals": "metricGoals",
        "name": "name",
        "online_ab_config": "onlineAbConfig",
        "project": "project",
        "randomization_salt": "randomizationSalt",
        "sampling_rate": "samplingRate",
        "tags": "tags",
        "treatments": "treatments",
    },
)
class CfnExperimentProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        metric_goals: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnExperiment.MetricGoalObjectProperty, _IResolvable_a771d0ef]]],
        name: builtins.str,
        online_ab_config: typing.Union[CfnExperiment.OnlineAbConfigObjectProperty, _IResolvable_a771d0ef],
        project: builtins.str,
        randomization_salt: typing.Optional[builtins.str] = None,
        sampling_rate: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
        treatments: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnExperiment.TreatmentObjectProperty, _IResolvable_a771d0ef]]],
    ) -> None:
        '''Properties for defining a ``AWS::Evidently::Experiment``.

        :param description: ``AWS::Evidently::Experiment.Description``.
        :param metric_goals: ``AWS::Evidently::Experiment.MetricGoals``.
        :param name: ``AWS::Evidently::Experiment.Name``.
        :param online_ab_config: ``AWS::Evidently::Experiment.OnlineAbConfig``.
        :param project: ``AWS::Evidently::Experiment.Project``.
        :param randomization_salt: ``AWS::Evidently::Experiment.RandomizationSalt``.
        :param sampling_rate: ``AWS::Evidently::Experiment.SamplingRate``.
        :param tags: ``AWS::Evidently::Experiment.Tags``.
        :param treatments: ``AWS::Evidently::Experiment.Treatments``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_evidently as evidently
            
            cfn_experiment_props = evidently.CfnExperimentProps(
                metric_goals=[evidently.CfnExperiment.MetricGoalObjectProperty(
                    desired_change="desiredChange",
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    value_key="valueKey",
            
                    # the properties below are optional
                    unit_label="unitLabel"
                )],
                name="name",
                online_ab_config=evidently.CfnExperiment.OnlineAbConfigObjectProperty(
                    control_treatment_name="controlTreatmentName",
                    treatment_weights=[evidently.CfnExperiment.TreatmentToWeightProperty(
                        split_weight=123,
                        treatment="treatment"
                    )]
                ),
                project="project",
                treatments=[evidently.CfnExperiment.TreatmentObjectProperty(
                    feature="feature",
                    treatment_name="treatmentName",
                    variation="variation",
            
                    # the properties below are optional
                    description="description"
                )],
            
                # the properties below are optional
                description="description",
                randomization_salt="randomizationSalt",
                sampling_rate=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "metric_goals": metric_goals,
            "name": name,
            "online_ab_config": online_ab_config,
            "project": project,
            "treatments": treatments,
        }
        if description is not None:
            self._values["description"] = description
        if randomization_salt is not None:
            self._values["randomization_salt"] = randomization_salt
        if sampling_rate is not None:
            self._values["sampling_rate"] = sampling_rate
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Experiment.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_goals(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnExperiment.MetricGoalObjectProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Experiment.MetricGoals``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-metricgoals
        '''
        result = self._values.get("metric_goals")
        assert result is not None, "Required property 'metric_goals' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnExperiment.MetricGoalObjectProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Experiment.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def online_ab_config(
        self,
    ) -> typing.Union[CfnExperiment.OnlineAbConfigObjectProperty, _IResolvable_a771d0ef]:
        '''``AWS::Evidently::Experiment.OnlineAbConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-onlineabconfig
        '''
        result = self._values.get("online_ab_config")
        assert result is not None, "Required property 'online_ab_config' is missing"
        return typing.cast(typing.Union[CfnExperiment.OnlineAbConfigObjectProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def project(self) -> builtins.str:
        '''``AWS::Evidently::Experiment.Project``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-project
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def randomization_salt(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Experiment.RandomizationSalt``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-randomizationsalt
        '''
        result = self._values.get("randomization_salt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_rate(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Evidently::Experiment.SamplingRate``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-samplingrate
        '''
        result = self._values.get("sampling_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Evidently::Experiment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def treatments(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnExperiment.TreatmentObjectProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Experiment.Treatments``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-experiment.html#cfn-evidently-experiment-treatments
        '''
        result = self._values.get("treatments")
        assert result is not None, "Required property 'treatments' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnExperiment.TreatmentObjectProperty, _IResolvable_a771d0ef]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExperimentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFeature(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_evidently.CfnFeature",
):
    '''A CloudFormation ``AWS::Evidently::Feature``.

    :cloudformationResource: AWS::Evidently::Feature
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_evidently as evidently
        
        cfn_feature = evidently.CfnFeature(self, "MyCfnFeature",
            name="name",
            project="project",
            variations=[evidently.CfnFeature.VariationObjectProperty(
                boolean_value=False,
                double_value=123,
                long_value=123,
                string_value="stringValue",
                variation_name="variationName"
            )],
        
            # the properties below are optional
            default_variation="defaultVariation",
            description="description",
            entity_overrides=[evidently.CfnFeature.EntityOverrideProperty(
                entity_id="entityId",
                variation="variation"
            )],
            evaluation_strategy="evaluationStrategy",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        default_variation: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        entity_overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnFeature.EntityOverrideProperty", _IResolvable_a771d0ef]]]] = None,
        evaluation_strategy: typing.Optional[builtins.str] = None,
        name: builtins.str,
        project: builtins.str,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
        variations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnFeature.VariationObjectProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        '''Create a new ``AWS::Evidently::Feature``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_variation: ``AWS::Evidently::Feature.DefaultVariation``.
        :param description: ``AWS::Evidently::Feature.Description``.
        :param entity_overrides: ``AWS::Evidently::Feature.EntityOverrides``.
        :param evaluation_strategy: ``AWS::Evidently::Feature.EvaluationStrategy``.
        :param name: ``AWS::Evidently::Feature.Name``.
        :param project: ``AWS::Evidently::Feature.Project``.
        :param tags: ``AWS::Evidently::Feature.Tags``.
        :param variations: ``AWS::Evidently::Feature.Variations``.
        '''
        props = CfnFeatureProps(
            default_variation=default_variation,
            description=description,
            entity_overrides=entity_overrides,
            evaluation_strategy=evaluation_strategy,
            name=name,
            project=project,
            tags=tags,
            variations=variations,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="defaultVariation")
    def default_variation(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Feature.DefaultVariation``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-defaultvariation
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultVariation"))

    @default_variation.setter
    def default_variation(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultVariation", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Feature.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="entityOverrides")
    def entity_overrides(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFeature.EntityOverrideProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Evidently::Feature.EntityOverrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-entityoverrides
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFeature.EntityOverrideProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "entityOverrides"))

    @entity_overrides.setter
    def entity_overrides(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFeature.EntityOverrideProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "entityOverrides", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="evaluationStrategy")
    def evaluation_strategy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Feature.EvaluationStrategy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-evaluationstrategy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationStrategy"))

    @evaluation_strategy.setter
    def evaluation_strategy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "evaluationStrategy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Feature.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        '''``AWS::Evidently::Feature.Project``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-project
        '''
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        jsii.set(self, "project", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Evidently::Feature.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variations")
    def variations(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFeature.VariationObjectProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Feature.Variations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-variations
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFeature.VariationObjectProperty", _IResolvable_a771d0ef]]], jsii.get(self, "variations"))

    @variations.setter
    def variations(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFeature.VariationObjectProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "variations", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnFeature.EntityOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"entity_id": "entityId", "variation": "variation"},
    )
    class EntityOverrideProperty:
        def __init__(
            self,
            *,
            entity_id: typing.Optional[builtins.str] = None,
            variation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param entity_id: ``CfnFeature.EntityOverrideProperty.EntityId``.
            :param variation: ``CfnFeature.EntityOverrideProperty.Variation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-entityoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                entity_override_property = evidently.CfnFeature.EntityOverrideProperty(
                    entity_id="entityId",
                    variation="variation"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if entity_id is not None:
                self._values["entity_id"] = entity_id
            if variation is not None:
                self._values["variation"] = variation

        @builtins.property
        def entity_id(self) -> typing.Optional[builtins.str]:
            '''``CfnFeature.EntityOverrideProperty.EntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-entityoverride.html#cfn-evidently-feature-entityoverride-entityid
            '''
            result = self._values.get("entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variation(self) -> typing.Optional[builtins.str]:
            '''``CfnFeature.EntityOverrideProperty.Variation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-entityoverride.html#cfn-evidently-feature-entityoverride-variation
            '''
            result = self._values.get("variation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnFeature.VariationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "long_value": "longValue",
            "string_value": "stringValue",
            "variation_name": "variationName",
        },
    )
    class VariationObjectProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            long_value: typing.Optional[jsii.Number] = None,
            string_value: typing.Optional[builtins.str] = None,
            variation_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param boolean_value: ``CfnFeature.VariationObjectProperty.BooleanValue``.
            :param double_value: ``CfnFeature.VariationObjectProperty.DoubleValue``.
            :param long_value: ``CfnFeature.VariationObjectProperty.LongValue``.
            :param string_value: ``CfnFeature.VariationObjectProperty.StringValue``.
            :param variation_name: ``CfnFeature.VariationObjectProperty.VariationName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                variation_object_property = evidently.CfnFeature.VariationObjectProperty(
                    boolean_value=False,
                    double_value=123,
                    long_value=123,
                    string_value="stringValue",
                    variation_name="variationName"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if string_value is not None:
                self._values["string_value"] = string_value
            if variation_name is not None:
                self._values["variation_name"] = variation_name

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFeature.VariationObjectProperty.BooleanValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''``CfnFeature.VariationObjectProperty.DoubleValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''``CfnFeature.VariationObjectProperty.LongValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''``CfnFeature.VariationObjectProperty.StringValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variation_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFeature.VariationObjectProperty.VariationName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-feature-variationobject.html#cfn-evidently-feature-variationobject-variationname
            '''
            result = self._values.get("variation_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_evidently.CfnFeatureProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_variation": "defaultVariation",
        "description": "description",
        "entity_overrides": "entityOverrides",
        "evaluation_strategy": "evaluationStrategy",
        "name": "name",
        "project": "project",
        "tags": "tags",
        "variations": "variations",
    },
)
class CfnFeatureProps:
    def __init__(
        self,
        *,
        default_variation: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        entity_overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnFeature.EntityOverrideProperty, _IResolvable_a771d0ef]]]] = None,
        evaluation_strategy: typing.Optional[builtins.str] = None,
        name: builtins.str,
        project: builtins.str,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
        variations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnFeature.VariationObjectProperty, _IResolvable_a771d0ef]]],
    ) -> None:
        '''Properties for defining a ``AWS::Evidently::Feature``.

        :param default_variation: ``AWS::Evidently::Feature.DefaultVariation``.
        :param description: ``AWS::Evidently::Feature.Description``.
        :param entity_overrides: ``AWS::Evidently::Feature.EntityOverrides``.
        :param evaluation_strategy: ``AWS::Evidently::Feature.EvaluationStrategy``.
        :param name: ``AWS::Evidently::Feature.Name``.
        :param project: ``AWS::Evidently::Feature.Project``.
        :param tags: ``AWS::Evidently::Feature.Tags``.
        :param variations: ``AWS::Evidently::Feature.Variations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_evidently as evidently
            
            cfn_feature_props = evidently.CfnFeatureProps(
                name="name",
                project="project",
                variations=[evidently.CfnFeature.VariationObjectProperty(
                    boolean_value=False,
                    double_value=123,
                    long_value=123,
                    string_value="stringValue",
                    variation_name="variationName"
                )],
            
                # the properties below are optional
                default_variation="defaultVariation",
                description="description",
                entity_overrides=[evidently.CfnFeature.EntityOverrideProperty(
                    entity_id="entityId",
                    variation="variation"
                )],
                evaluation_strategy="evaluationStrategy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "project": project,
            "variations": variations,
        }
        if default_variation is not None:
            self._values["default_variation"] = default_variation
        if description is not None:
            self._values["description"] = description
        if entity_overrides is not None:
            self._values["entity_overrides"] = entity_overrides
        if evaluation_strategy is not None:
            self._values["evaluation_strategy"] = evaluation_strategy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_variation(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Feature.DefaultVariation``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-defaultvariation
        '''
        result = self._values.get("default_variation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Feature.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_overrides(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFeature.EntityOverrideProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Evidently::Feature.EntityOverrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-entityoverrides
        '''
        result = self._values.get("entity_overrides")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFeature.EntityOverrideProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def evaluation_strategy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Feature.EvaluationStrategy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-evaluationstrategy
        '''
        result = self._values.get("evaluation_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Feature.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''``AWS::Evidently::Feature.Project``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-project
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Evidently::Feature.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def variations(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFeature.VariationObjectProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Feature.Variations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-feature.html#cfn-evidently-feature-variations
        '''
        result = self._values.get("variations")
        assert result is not None, "Required property 'variations' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFeature.VariationObjectProperty, _IResolvable_a771d0ef]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFeatureProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLaunch(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_evidently.CfnLaunch",
):
    '''A CloudFormation ``AWS::Evidently::Launch``.

    :cloudformationResource: AWS::Evidently::Launch
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_evidently as evidently
        
        cfn_launch = evidently.CfnLaunch(self, "MyCfnLaunch",
            groups=[evidently.CfnLaunch.LaunchGroupObjectProperty(
                feature="feature",
                group_name="groupName",
                variation="variation",
        
                # the properties below are optional
                description="description"
            )],
            name="name",
            project="project",
            scheduled_splits_config=[evidently.CfnLaunch.StepConfigProperty(
                group_weights=[evidently.CfnLaunch.GroupToWeightProperty(
                    group_name="groupName",
                    split_weight=123
                )],
                start_time="startTime"
            )],
        
            # the properties below are optional
            description="description",
            metric_monitors=[evidently.CfnLaunch.MetricDefinitionObjectProperty(
                entity_id_key="entityIdKey",
                event_pattern="eventPattern",
                metric_name="metricName",
                value_key="valueKey",
        
                # the properties below are optional
                unit_label="unitLabel"
            )],
            randomization_salt="randomizationSalt",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnLaunch.LaunchGroupObjectProperty", _IResolvable_a771d0ef]]],
        metric_monitors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnLaunch.MetricDefinitionObjectProperty", _IResolvable_a771d0ef]]]] = None,
        name: builtins.str,
        project: builtins.str,
        randomization_salt: typing.Optional[builtins.str] = None,
        scheduled_splits_config: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnLaunch.StepConfigProperty", _IResolvable_a771d0ef]]],
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Evidently::Launch``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Evidently::Launch.Description``.
        :param groups: ``AWS::Evidently::Launch.Groups``.
        :param metric_monitors: ``AWS::Evidently::Launch.MetricMonitors``.
        :param name: ``AWS::Evidently::Launch.Name``.
        :param project: ``AWS::Evidently::Launch.Project``.
        :param randomization_salt: ``AWS::Evidently::Launch.RandomizationSalt``.
        :param scheduled_splits_config: ``AWS::Evidently::Launch.ScheduledSplitsConfig``.
        :param tags: ``AWS::Evidently::Launch.Tags``.
        '''
        props = CfnLaunchProps(
            description=description,
            groups=groups,
            metric_monitors=metric_monitors,
            name=name,
            project=project,
            randomization_salt=randomization_salt,
            scheduled_splits_config=scheduled_splits_config,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
        '''``AWS::Evidently::Launch.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="groups")
    def groups(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.LaunchGroupObjectProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Launch.Groups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-groups
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.LaunchGroupObjectProperty", _IResolvable_a771d0ef]]], jsii.get(self, "groups"))

    @groups.setter
    def groups(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.LaunchGroupObjectProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "groups", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metricMonitors")
    def metric_monitors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.MetricDefinitionObjectProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Evidently::Launch.MetricMonitors``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-metricmonitors
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.MetricDefinitionObjectProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "metricMonitors"))

    @metric_monitors.setter
    def metric_monitors(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.MetricDefinitionObjectProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "metricMonitors", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Launch.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        '''``AWS::Evidently::Launch.Project``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-project
        '''
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        jsii.set(self, "project", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="randomizationSalt")
    def randomization_salt(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Launch.RandomizationSalt``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-randomizationsalt
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "randomizationSalt"))

    @randomization_salt.setter
    def randomization_salt(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "randomizationSalt", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scheduledSplitsConfig")
    def scheduled_splits_config(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.StepConfigProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Launch.ScheduledSplitsConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-scheduledsplitsconfig
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.StepConfigProperty", _IResolvable_a771d0ef]]], jsii.get(self, "scheduledSplitsConfig"))

    @scheduled_splits_config.setter
    def scheduled_splits_config(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.StepConfigProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "scheduledSplitsConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Evidently::Launch.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnLaunch.GroupToWeightProperty",
        jsii_struct_bases=[],
        name_mapping={"group_name": "groupName", "split_weight": "splitWeight"},
    )
    class GroupToWeightProperty:
        def __init__(
            self,
            *,
            group_name: builtins.str,
            split_weight: jsii.Number,
        ) -> None:
            '''
            :param group_name: ``CfnLaunch.GroupToWeightProperty.GroupName``.
            :param split_weight: ``CfnLaunch.GroupToWeightProperty.SplitWeight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-grouptoweight.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                group_to_weight_property = evidently.CfnLaunch.GroupToWeightProperty(
                    group_name="groupName",
                    split_weight=123
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "group_name": group_name,
                "split_weight": split_weight,
            }

        @builtins.property
        def group_name(self) -> builtins.str:
            '''``CfnLaunch.GroupToWeightProperty.GroupName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-grouptoweight.html#cfn-evidently-launch-grouptoweight-groupname
            '''
            result = self._values.get("group_name")
            assert result is not None, "Required property 'group_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def split_weight(self) -> jsii.Number:
            '''``CfnLaunch.GroupToWeightProperty.SplitWeight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-grouptoweight.html#cfn-evidently-launch-grouptoweight-splitweight
            '''
            result = self._values.get("split_weight")
            assert result is not None, "Required property 'split_weight' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupToWeightProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnLaunch.LaunchGroupObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "feature": "feature",
            "group_name": "groupName",
            "variation": "variation",
        },
    )
    class LaunchGroupObjectProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            feature: builtins.str,
            group_name: builtins.str,
            variation: builtins.str,
        ) -> None:
            '''
            :param description: ``CfnLaunch.LaunchGroupObjectProperty.Description``.
            :param feature: ``CfnLaunch.LaunchGroupObjectProperty.Feature``.
            :param group_name: ``CfnLaunch.LaunchGroupObjectProperty.GroupName``.
            :param variation: ``CfnLaunch.LaunchGroupObjectProperty.Variation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                launch_group_object_property = evidently.CfnLaunch.LaunchGroupObjectProperty(
                    feature="feature",
                    group_name="groupName",
                    variation="variation",
                
                    # the properties below are optional
                    description="description"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "feature": feature,
                "group_name": group_name,
                "variation": variation,
            }
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnLaunch.LaunchGroupObjectProperty.Description``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def feature(self) -> builtins.str:
            '''``CfnLaunch.LaunchGroupObjectProperty.Feature``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-feature
            '''
            result = self._values.get("feature")
            assert result is not None, "Required property 'feature' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_name(self) -> builtins.str:
            '''``CfnLaunch.LaunchGroupObjectProperty.GroupName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-groupname
            '''
            result = self._values.get("group_name")
            assert result is not None, "Required property 'group_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def variation(self) -> builtins.str:
            '''``CfnLaunch.LaunchGroupObjectProperty.Variation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-launchgroupobject.html#cfn-evidently-launch-launchgroupobject-variation
            '''
            result = self._values.get("variation")
            assert result is not None, "Required property 'variation' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchGroupObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnLaunch.MetricDefinitionObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "entity_id_key": "entityIdKey",
            "event_pattern": "eventPattern",
            "metric_name": "metricName",
            "unit_label": "unitLabel",
            "value_key": "valueKey",
        },
    )
    class MetricDefinitionObjectProperty:
        def __init__(
            self,
            *,
            entity_id_key: builtins.str,
            event_pattern: builtins.str,
            metric_name: builtins.str,
            unit_label: typing.Optional[builtins.str] = None,
            value_key: builtins.str,
        ) -> None:
            '''
            :param entity_id_key: ``CfnLaunch.MetricDefinitionObjectProperty.EntityIdKey``.
            :param event_pattern: ``CfnLaunch.MetricDefinitionObjectProperty.EventPattern``.
            :param metric_name: ``CfnLaunch.MetricDefinitionObjectProperty.MetricName``.
            :param unit_label: ``CfnLaunch.MetricDefinitionObjectProperty.UnitLabel``.
            :param value_key: ``CfnLaunch.MetricDefinitionObjectProperty.ValueKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                metric_definition_object_property = evidently.CfnLaunch.MetricDefinitionObjectProperty(
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    value_key="valueKey",
                
                    # the properties below are optional
                    unit_label="unitLabel"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "entity_id_key": entity_id_key,
                "event_pattern": event_pattern,
                "metric_name": metric_name,
                "value_key": value_key,
            }
            if unit_label is not None:
                self._values["unit_label"] = unit_label

        @builtins.property
        def entity_id_key(self) -> builtins.str:
            '''``CfnLaunch.MetricDefinitionObjectProperty.EntityIdKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-entityidkey
            '''
            result = self._values.get("entity_id_key")
            assert result is not None, "Required property 'entity_id_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def event_pattern(self) -> builtins.str:
            '''``CfnLaunch.MetricDefinitionObjectProperty.EventPattern``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-eventpattern
            '''
            result = self._values.get("event_pattern")
            assert result is not None, "Required property 'event_pattern' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''``CfnLaunch.MetricDefinitionObjectProperty.MetricName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def unit_label(self) -> typing.Optional[builtins.str]:
            '''``CfnLaunch.MetricDefinitionObjectProperty.UnitLabel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-unitlabel
            '''
            result = self._values.get("unit_label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_key(self) -> builtins.str:
            '''``CfnLaunch.MetricDefinitionObjectProperty.ValueKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-metricdefinitionobject.html#cfn-evidently-launch-metricdefinitionobject-valuekey
            '''
            result = self._values.get("value_key")
            assert result is not None, "Required property 'value_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDefinitionObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnLaunch.StepConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"group_weights": "groupWeights", "start_time": "startTime"},
    )
    class StepConfigProperty:
        def __init__(
            self,
            *,
            group_weights: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnLaunch.GroupToWeightProperty", _IResolvable_a771d0ef]]],
            start_time: builtins.str,
        ) -> None:
            '''
            :param group_weights: ``CfnLaunch.StepConfigProperty.GroupWeights``.
            :param start_time: ``CfnLaunch.StepConfigProperty.StartTime``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-stepconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                step_config_property = evidently.CfnLaunch.StepConfigProperty(
                    group_weights=[evidently.CfnLaunch.GroupToWeightProperty(
                        group_name="groupName",
                        split_weight=123
                    )],
                    start_time="startTime"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "group_weights": group_weights,
                "start_time": start_time,
            }

        @builtins.property
        def group_weights(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.GroupToWeightProperty", _IResolvable_a771d0ef]]]:
            '''``CfnLaunch.StepConfigProperty.GroupWeights``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-stepconfig.html#cfn-evidently-launch-stepconfig-groupweights
            '''
            result = self._values.get("group_weights")
            assert result is not None, "Required property 'group_weights' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLaunch.GroupToWeightProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def start_time(self) -> builtins.str:
            '''``CfnLaunch.StepConfigProperty.StartTime``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-launch-stepconfig.html#cfn-evidently-launch-stepconfig-starttime
            '''
            result = self._values.get("start_time")
            assert result is not None, "Required property 'start_time' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StepConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_evidently.CfnLaunchProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "groups": "groups",
        "metric_monitors": "metricMonitors",
        "name": "name",
        "project": "project",
        "randomization_salt": "randomizationSalt",
        "scheduled_splits_config": "scheduledSplitsConfig",
        "tags": "tags",
    },
)
class CfnLaunchProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnLaunch.LaunchGroupObjectProperty, _IResolvable_a771d0ef]]],
        metric_monitors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnLaunch.MetricDefinitionObjectProperty, _IResolvable_a771d0ef]]]] = None,
        name: builtins.str,
        project: builtins.str,
        randomization_salt: typing.Optional[builtins.str] = None,
        scheduled_splits_config: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnLaunch.StepConfigProperty, _IResolvable_a771d0ef]]],
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Evidently::Launch``.

        :param description: ``AWS::Evidently::Launch.Description``.
        :param groups: ``AWS::Evidently::Launch.Groups``.
        :param metric_monitors: ``AWS::Evidently::Launch.MetricMonitors``.
        :param name: ``AWS::Evidently::Launch.Name``.
        :param project: ``AWS::Evidently::Launch.Project``.
        :param randomization_salt: ``AWS::Evidently::Launch.RandomizationSalt``.
        :param scheduled_splits_config: ``AWS::Evidently::Launch.ScheduledSplitsConfig``.
        :param tags: ``AWS::Evidently::Launch.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_evidently as evidently
            
            cfn_launch_props = evidently.CfnLaunchProps(
                groups=[evidently.CfnLaunch.LaunchGroupObjectProperty(
                    feature="feature",
                    group_name="groupName",
                    variation="variation",
            
                    # the properties below are optional
                    description="description"
                )],
                name="name",
                project="project",
                scheduled_splits_config=[evidently.CfnLaunch.StepConfigProperty(
                    group_weights=[evidently.CfnLaunch.GroupToWeightProperty(
                        group_name="groupName",
                        split_weight=123
                    )],
                    start_time="startTime"
                )],
            
                # the properties below are optional
                description="description",
                metric_monitors=[evidently.CfnLaunch.MetricDefinitionObjectProperty(
                    entity_id_key="entityIdKey",
                    event_pattern="eventPattern",
                    metric_name="metricName",
                    value_key="valueKey",
            
                    # the properties below are optional
                    unit_label="unitLabel"
                )],
                randomization_salt="randomizationSalt",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "groups": groups,
            "name": name,
            "project": project,
            "scheduled_splits_config": scheduled_splits_config,
        }
        if description is not None:
            self._values["description"] = description
        if metric_monitors is not None:
            self._values["metric_monitors"] = metric_monitors
        if randomization_salt is not None:
            self._values["randomization_salt"] = randomization_salt
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Launch.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLaunch.LaunchGroupObjectProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Launch.Groups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-groups
        '''
        result = self._values.get("groups")
        assert result is not None, "Required property 'groups' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLaunch.LaunchGroupObjectProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def metric_monitors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLaunch.MetricDefinitionObjectProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Evidently::Launch.MetricMonitors``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-metricmonitors
        '''
        result = self._values.get("metric_monitors")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLaunch.MetricDefinitionObjectProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Launch.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''``AWS::Evidently::Launch.Project``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-project
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def randomization_salt(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Launch.RandomizationSalt``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-randomizationsalt
        '''
        result = self._values.get("randomization_salt")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_splits_config(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLaunch.StepConfigProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::Evidently::Launch.ScheduledSplitsConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-scheduledsplitsconfig
        '''
        result = self._values.get("scheduled_splits_config")
        assert result is not None, "Required property 'scheduled_splits_config' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLaunch.StepConfigProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Evidently::Launch.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-launch.html#cfn-evidently-launch-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnProject(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_evidently.CfnProject",
):
    '''A CloudFormation ``AWS::Evidently::Project``.

    :cloudformationResource: AWS::Evidently::Project
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_evidently as evidently
        
        cfn_project = evidently.CfnProject(self, "MyCfnProject",
            name="name",
        
            # the properties below are optional
            data_delivery=evidently.CfnProject.DataDeliveryObjectProperty(
                log_group="logGroup",
                s3=evidently.CfnProject.S3DestinationProperty(
                    bucket_name="bucketName",
        
                    # the properties below are optional
                    prefix="prefix"
                )
            ),
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        data_delivery: typing.Optional[typing.Union["CfnProject.DataDeliveryObjectProperty", _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        name: builtins.str,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Evidently::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_delivery: ``AWS::Evidently::Project.DataDelivery``.
        :param description: ``AWS::Evidently::Project.Description``.
        :param name: ``AWS::Evidently::Project.Name``.
        :param tags: ``AWS::Evidently::Project.Tags``.
        '''
        props = CfnProjectProps(
            data_delivery=data_delivery, description=description, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="dataDelivery")
    def data_delivery(
        self,
    ) -> typing.Optional[typing.Union["CfnProject.DataDeliveryObjectProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Evidently::Project.DataDelivery``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-datadelivery
        '''
        return typing.cast(typing.Optional[typing.Union["CfnProject.DataDeliveryObjectProperty", _IResolvable_a771d0ef]], jsii.get(self, "dataDelivery"))

    @data_delivery.setter
    def data_delivery(
        self,
        value: typing.Optional[typing.Union["CfnProject.DataDeliveryObjectProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "dataDelivery", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Project.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Project.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Evidently::Project.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnProject.DataDeliveryObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group": "logGroup", "s3": "s3"},
    )
    class DataDeliveryObjectProperty:
        def __init__(
            self,
            *,
            log_group: typing.Optional[builtins.str] = None,
            s3: typing.Optional[typing.Union["CfnProject.S3DestinationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param log_group: ``CfnProject.DataDeliveryObjectProperty.LogGroup``.
            :param s3: ``CfnProject.DataDeliveryObjectProperty.S3``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-datadeliveryobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                data_delivery_object_property = evidently.CfnProject.DataDeliveryObjectProperty(
                    log_group="logGroup",
                    s3=evidently.CfnProject.S3DestinationProperty(
                        bucket_name="bucketName",
                
                        # the properties below are optional
                        prefix="prefix"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if log_group is not None:
                self._values["log_group"] = log_group
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''``CfnProject.DataDeliveryObjectProperty.LogGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-datadeliveryobject.html#cfn-evidently-project-datadeliveryobject-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["CfnProject.S3DestinationProperty", _IResolvable_a771d0ef]]:
            '''``CfnProject.DataDeliveryObjectProperty.S3``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-datadeliveryobject.html#cfn-evidently-project-datadeliveryobject-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["CfnProject.S3DestinationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataDeliveryObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_evidently.CfnProject.S3DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "prefix": "prefix"},
    )
    class S3DestinationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_name: ``CfnProject.S3DestinationProperty.BucketName``.
            :param prefix: ``CfnProject.S3DestinationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-s3destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_evidently as evidently
                
                s3_destination_property = evidently.CfnProject.S3DestinationProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    prefix="prefix"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnProject.S3DestinationProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-s3destination.html#cfn-evidently-project-s3destination-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnProject.S3DestinationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evidently-project-s3destination.html#cfn-evidently-project-s3destination-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_evidently.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_delivery": "dataDelivery",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        data_delivery: typing.Optional[typing.Union[CfnProject.DataDeliveryObjectProperty, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        name: builtins.str,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Evidently::Project``.

        :param data_delivery: ``AWS::Evidently::Project.DataDelivery``.
        :param description: ``AWS::Evidently::Project.Description``.
        :param name: ``AWS::Evidently::Project.Name``.
        :param tags: ``AWS::Evidently::Project.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_evidently as evidently
            
            cfn_project_props = evidently.CfnProjectProps(
                name="name",
            
                # the properties below are optional
                data_delivery=evidently.CfnProject.DataDeliveryObjectProperty(
                    log_group="logGroup",
                    s3=evidently.CfnProject.S3DestinationProperty(
                        bucket_name="bucketName",
            
                        # the properties below are optional
                        prefix="prefix"
                    )
                ),
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if data_delivery is not None:
            self._values["data_delivery"] = data_delivery
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_delivery(
        self,
    ) -> typing.Optional[typing.Union[CfnProject.DataDeliveryObjectProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Evidently::Project.DataDelivery``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-datadelivery
        '''
        result = self._values.get("data_delivery")
        return typing.cast(typing.Optional[typing.Union[CfnProject.DataDeliveryObjectProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Evidently::Project.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Evidently::Project.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Evidently::Project.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evidently-project.html#cfn-evidently-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnExperiment",
    "CfnExperimentProps",
    "CfnFeature",
    "CfnFeatureProps",
    "CfnLaunch",
    "CfnLaunchProps",
    "CfnProject",
    "CfnProjectProps",
]

publication.publish()
