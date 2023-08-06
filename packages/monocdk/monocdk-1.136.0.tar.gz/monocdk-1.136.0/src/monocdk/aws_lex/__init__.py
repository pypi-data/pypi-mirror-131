'''
# AWS::Lex Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as lex
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Lex](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Lex.html).

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
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnBot(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lex.CfnBot",
):
    '''A CloudFormation ``AWS::Lex::Bot``.

    :cloudformationResource: AWS::Lex::Bot
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_lex as lex
        
        # data_privacy is of type object
        
        cfn_bot = lex.CfnBot(self, "MyCfnBot",
            data_privacy=data_privacy,
            idle_session_ttl_in_seconds=123,
            name="name",
            role_arn="roleArn",
        
            # the properties below are optional
            auto_build_bot_locales=False,
            bot_file_s3_location=lex.CfnBot.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_object_key="s3ObjectKey",
        
                # the properties below are optional
                s3_object_version="s3ObjectVersion"
            ),
            bot_locales=[lex.CfnBot.BotLocaleProperty(
                locale_id="localeId",
                nlu_confidence_threshold=123,
        
                # the properties below are optional
                description="description",
                intents=[lex.CfnBot.IntentProperty(
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                        enabled=False
                    ),
                    fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                        enabled=False,
        
                        # the properties below are optional
                        fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                            active=False,
        
                            # the properties below are optional
                            start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                delay_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_in_seconds=123,
                            update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                frequency_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        ),
                        post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                            failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            success_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        )
                    ),
                    input_contexts=[lex.CfnBot.InputContextProperty(
                        name="name"
                    )],
                    intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                        closing_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
        
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
        
                            # the properties below are optional
                            allow_interrupt=False
                        ),
        
                        # the properties below are optional
                        is_active=False
                    ),
                    intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                        declination_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
        
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
        
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            max_retries=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
        
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
        
                            # the properties below are optional
                            allow_interrupt=False
                        ),
        
                        # the properties below are optional
                        is_active=False
                    ),
                    kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                        kendra_index="kendraIndex",
        
                        # the properties below are optional
                        query_filter_string="queryFilterString",
                        query_filter_string_enabled=False
                    ),
                    output_contexts=[lex.CfnBot.OutputContextProperty(
                        name="name",
                        time_to_live_in_seconds=123,
                        turns_to_live=123
                    )],
                    parent_intent_signature="parentIntentSignature",
                    sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                        utterance="utterance"
                    )],
                    slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                        priority=123,
                        slot_name="slotName"
                    )],
                    slots=[lex.CfnBot.SlotProperty(
                        name="name",
                        slot_type_name="slotTypeName",
                        value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                            slot_constraint="slotConstraint",
        
                            # the properties below are optional
                            default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                    default_value="defaultValue"
                                )]
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                utterance="utterance"
                            )],
                            wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
        
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
        
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
        
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
        
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
        
                                # the properties below are optional
                                is_active=False,
                                still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
        
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                                    timeout_in_seconds=123,
        
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
        
                        # the properties below are optional
                        description="description",
                        multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                            allow_multiple_values=False
                        ),
                        obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                            obfuscation_setting_type="obfuscationSettingType"
                        )
                    )]
                )],
                slot_types=[lex.CfnBot.SlotTypeProperty(
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                        grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                            source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                s3_bucket_name="s3BucketName",
                                s3_object_key="s3ObjectKey",
        
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        )
                    ),
                    parent_slot_type_signature="parentSlotTypeSignature",
                    slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                        sample_value=lex.CfnBot.SampleValueProperty(
                            value="value"
                        ),
        
                        # the properties below are optional
                        synonyms=[lex.CfnBot.SampleValueProperty(
                            value="value"
                        )]
                    )],
                    value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                        resolution_strategy="resolutionStrategy",
        
                        # the properties below are optional
                        regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                            pattern="pattern"
                        )
                    )
                )],
                voice_settings=lex.CfnBot.VoiceSettingsProperty(
                    voice_id="voiceId"
                )
            )],
            bot_tags=[CfnTag(
                key="key",
                value="value"
            )],
            description="description",
            test_bot_alias_tags=[CfnTag(
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
        auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        bot_file_s3_location: typing.Optional[typing.Union["CfnBot.S3LocationProperty", _IResolvable_a771d0ef]] = None,
        bot_locales: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.BotLocaleProperty", _IResolvable_a771d0ef]]]] = None,
        bot_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
        data_privacy: typing.Any,
        description: typing.Optional[builtins.str] = None,
        idle_session_ttl_in_seconds: jsii.Number,
        name: builtins.str,
        role_arn: builtins.str,
        test_bot_alias_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Lex::Bot``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_build_bot_locales: ``AWS::Lex::Bot.AutoBuildBotLocales``.
        :param bot_file_s3_location: ``AWS::Lex::Bot.BotFileS3Location``.
        :param bot_locales: ``AWS::Lex::Bot.BotLocales``.
        :param bot_tags: ``AWS::Lex::Bot.BotTags``.
        :param data_privacy: ``AWS::Lex::Bot.DataPrivacy``.
        :param description: ``AWS::Lex::Bot.Description``.
        :param idle_session_ttl_in_seconds: ``AWS::Lex::Bot.IdleSessionTTLInSeconds``.
        :param name: ``AWS::Lex::Bot.Name``.
        :param role_arn: ``AWS::Lex::Bot.RoleArn``.
        :param test_bot_alias_tags: ``AWS::Lex::Bot.TestBotAliasTags``.
        '''
        props = CfnBotProps(
            auto_build_bot_locales=auto_build_bot_locales,
            bot_file_s3_location=bot_file_s3_location,
            bot_locales=bot_locales,
            bot_tags=bot_tags,
            data_privacy=data_privacy,
            description=description,
            idle_session_ttl_in_seconds=idle_session_ttl_in_seconds,
            name=name,
            role_arn=role_arn,
            test_bot_alias_tags=test_bot_alias_tags,
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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoBuildBotLocales")
    def auto_build_bot_locales(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Lex::Bot.AutoBuildBotLocales``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-autobuildbotlocales
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "autoBuildBotLocales"))

    @auto_build_bot_locales.setter
    def auto_build_bot_locales(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "autoBuildBotLocales", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botFileS3Location")
    def bot_file_s3_location(
        self,
    ) -> typing.Optional[typing.Union["CfnBot.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Lex::Bot.BotFileS3Location``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botfiles3location
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBot.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "botFileS3Location"))

    @bot_file_s3_location.setter
    def bot_file_s3_location(
        self,
        value: typing.Optional[typing.Union["CfnBot.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "botFileS3Location", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botLocales")
    def bot_locales(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.BotLocaleProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Lex::Bot.BotLocales``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botlocales
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.BotLocaleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "botLocales"))

    @bot_locales.setter
    def bot_locales(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.BotLocaleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "botLocales", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botTags")
    def bot_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''``AWS::Lex::Bot.BotTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-bottags
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], jsii.get(self, "botTags"))

    @bot_tags.setter
    def bot_tags(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]],
    ) -> None:
        jsii.set(self, "botTags", value)

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
    @jsii.member(jsii_name="dataPrivacy")
    def data_privacy(self) -> typing.Any:
        '''``AWS::Lex::Bot.DataPrivacy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-dataprivacy
        '''
        return typing.cast(typing.Any, jsii.get(self, "dataPrivacy"))

    @data_privacy.setter
    def data_privacy(self, value: typing.Any) -> None:
        jsii.set(self, "dataPrivacy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Lex::Bot.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idleSessionTtlInSeconds")
    def idle_session_ttl_in_seconds(self) -> jsii.Number:
        '''``AWS::Lex::Bot.IdleSessionTTLInSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-idlesessionttlinseconds
        '''
        return typing.cast(jsii.Number, jsii.get(self, "idleSessionTtlInSeconds"))

    @idle_session_ttl_in_seconds.setter
    def idle_session_ttl_in_seconds(self, value: jsii.Number) -> None:
        jsii.set(self, "idleSessionTtlInSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Lex::Bot.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''``AWS::Lex::Bot.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="testBotAliasTags")
    def test_bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''``AWS::Lex::Bot.TestBotAliasTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliastags
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], jsii.get(self, "testBotAliasTags"))

    @test_bot_alias_tags.setter
    def test_bot_alias_tags(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]],
    ) -> None:
        jsii.set(self, "testBotAliasTags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.BotLocaleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "intents": "intents",
            "locale_id": "localeId",
            "nlu_confidence_threshold": "nluConfidenceThreshold",
            "slot_types": "slotTypes",
            "voice_settings": "voiceSettings",
        },
    )
    class BotLocaleProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            intents: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.IntentProperty", _IResolvable_a771d0ef]]]] = None,
            locale_id: builtins.str,
            nlu_confidence_threshold: jsii.Number,
            slot_types: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SlotTypeProperty", _IResolvable_a771d0ef]]]] = None,
            voice_settings: typing.Optional[typing.Union["CfnBot.VoiceSettingsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param description: ``CfnBot.BotLocaleProperty.Description``.
            :param intents: ``CfnBot.BotLocaleProperty.Intents``.
            :param locale_id: ``CfnBot.BotLocaleProperty.LocaleId``.
            :param nlu_confidence_threshold: ``CfnBot.BotLocaleProperty.NluConfidenceThreshold``.
            :param slot_types: ``CfnBot.BotLocaleProperty.SlotTypes``.
            :param voice_settings: ``CfnBot.BotLocaleProperty.VoiceSettings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                bot_locale_property = lex.CfnBot.BotLocaleProperty(
                    locale_id="localeId",
                    nlu_confidence_threshold=123,
                
                    # the properties below are optional
                    description="description",
                    intents=[lex.CfnBot.IntentProperty(
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                            enabled=False
                        ),
                        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                            enabled=False,
                
                            # the properties below are optional
                            fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                                active=False,
                
                                # the properties below are optional
                                start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                    delay_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_in_seconds=123,
                                update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            ),
                            post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                                failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                success_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
                        input_contexts=[lex.CfnBot.InputContextProperty(
                            name="name"
                        )],
                        intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                            closing_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                
                            # the properties below are optional
                            is_active=False
                        ),
                        intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                            declination_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                
                            # the properties below are optional
                            is_active=False
                        ),
                        kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                            kendra_index="kendraIndex",
                
                            # the properties below are optional
                            query_filter_string="queryFilterString",
                            query_filter_string_enabled=False
                        ),
                        output_contexts=[lex.CfnBot.OutputContextProperty(
                            name="name",
                            time_to_live_in_seconds=123,
                            turns_to_live=123
                        )],
                        parent_intent_signature="parentIntentSignature",
                        sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                            utterance="utterance"
                        )],
                        slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                            priority=123,
                            slot_name="slotName"
                        )],
                        slots=[lex.CfnBot.SlotProperty(
                            name="name",
                            slot_type_name="slotTypeName",
                            value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                                slot_constraint="slotConstraint",
                
                                # the properties below are optional
                                default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                    default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                        default_value="defaultValue"
                                    )]
                                ),
                                prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                    max_retries=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                    utterance="utterance"
                                )],
                                wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                    continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
                                    waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
                
                                    # the properties below are optional
                                    is_active=False,
                                    still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                        frequency_in_seconds=123,
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                                        timeout_in_seconds=123,
                
                                        # the properties below are optional
                                        allow_interrupt=False
                                    )
                                )
                            ),
                
                            # the properties below are optional
                            description="description",
                            multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                                allow_multiple_values=False
                            ),
                            obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                                obfuscation_setting_type="obfuscationSettingType"
                            )
                        )]
                    )],
                    slot_types=[lex.CfnBot.SlotTypeProperty(
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                            grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                                source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                    s3_bucket_name="s3BucketName",
                                    s3_object_key="s3ObjectKey",
                
                                    # the properties below are optional
                                    kms_key_arn="kmsKeyArn"
                                )
                            )
                        ),
                        parent_slot_type_signature="parentSlotTypeSignature",
                        slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                            sample_value=lex.CfnBot.SampleValueProperty(
                                value="value"
                            ),
                
                            # the properties below are optional
                            synonyms=[lex.CfnBot.SampleValueProperty(
                                value="value"
                            )]
                        )],
                        value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                            resolution_strategy="resolutionStrategy",
                
                            # the properties below are optional
                            regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                                pattern="pattern"
                            )
                        )
                    )],
                    voice_settings=lex.CfnBot.VoiceSettingsProperty(
                        voice_id="voiceId"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "locale_id": locale_id,
                "nlu_confidence_threshold": nlu_confidence_threshold,
            }
            if description is not None:
                self._values["description"] = description
            if intents is not None:
                self._values["intents"] = intents
            if slot_types is not None:
                self._values["slot_types"] = slot_types
            if voice_settings is not None:
                self._values["voice_settings"] = voice_settings

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.BotLocaleProperty.Description``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def intents(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.IntentProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.BotLocaleProperty.Intents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-intents
            '''
            result = self._values.get("intents")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.IntentProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def locale_id(self) -> builtins.str:
            '''``CfnBot.BotLocaleProperty.LocaleId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-localeid
            '''
            result = self._values.get("locale_id")
            assert result is not None, "Required property 'locale_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def nlu_confidence_threshold(self) -> jsii.Number:
            '''``CfnBot.BotLocaleProperty.NluConfidenceThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-nluconfidencethreshold
            '''
            result = self._values.get("nlu_confidence_threshold")
            assert result is not None, "Required property 'nlu_confidence_threshold' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def slot_types(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotTypeProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.BotLocaleProperty.SlotTypes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-slottypes
            '''
            result = self._values.get("slot_types")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotTypeProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def voice_settings(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.VoiceSettingsProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.BotLocaleProperty.VoiceSettings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-voicesettings
            '''
            result = self._values.get("voice_settings")
            return typing.cast(typing.Optional[typing.Union["CfnBot.VoiceSettingsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotLocaleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.ButtonProperty",
        jsii_struct_bases=[],
        name_mapping={"text": "text", "value": "value"},
    )
    class ButtonProperty:
        def __init__(self, *, text: builtins.str, value: builtins.str) -> None:
            '''
            :param text: ``CfnBot.ButtonProperty.Text``.
            :param value: ``CfnBot.ButtonProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                button_property = lex.CfnBot.ButtonProperty(
                    text="text",
                    value="value"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "text": text,
                "value": value,
            }

        @builtins.property
        def text(self) -> builtins.str:
            '''``CfnBot.ButtonProperty.Text``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html#cfn-lex-bot-button-text
            '''
            result = self._values.get("text")
            assert result is not None, "Required property 'text' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBot.ButtonProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html#cfn-lex-bot-button-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.CustomPayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class CustomPayloadProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''
            :param value: ``CfnBot.CustomPayloadProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-custompayload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                custom_payload_property = lex.CfnBot.CustomPayloadProperty(
                    value="value"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBot.CustomPayloadProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-custompayload.html#cfn-lex-bot-custompayload-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.DialogCodeHookSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class DialogCodeHookSettingProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param enabled: ``CfnBot.DialogCodeHookSettingProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehooksetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                dialog_code_hook_setting_property = lex.CfnBot.DialogCodeHookSettingProperty(
                    enabled=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnBot.DialogCodeHookSettingProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehooksetting.html#cfn-lex-bot-dialogcodehooksetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialogCodeHookSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.ExternalSourceSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"grammar_slot_type_setting": "grammarSlotTypeSetting"},
    )
    class ExternalSourceSettingProperty:
        def __init__(
            self,
            *,
            grammar_slot_type_setting: typing.Optional[typing.Union["CfnBot.GrammarSlotTypeSettingProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param grammar_slot_type_setting: ``CfnBot.ExternalSourceSettingProperty.GrammarSlotTypeSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-externalsourcesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                external_source_setting_property = lex.CfnBot.ExternalSourceSettingProperty(
                    grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                        source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                            s3_bucket_name="s3BucketName",
                            s3_object_key="s3ObjectKey",
                
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn"
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if grammar_slot_type_setting is not None:
                self._values["grammar_slot_type_setting"] = grammar_slot_type_setting

        @builtins.property
        def grammar_slot_type_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.GrammarSlotTypeSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.ExternalSourceSettingProperty.GrammarSlotTypeSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-externalsourcesetting.html#cfn-lex-bot-externalsourcesetting-grammarslottypesetting
            '''
            result = self._values.get("grammar_slot_type_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBot.GrammarSlotTypeSettingProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExternalSourceSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.FulfillmentCodeHookSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "fulfillment_updates_specification": "fulfillmentUpdatesSpecification",
            "post_fulfillment_status_specification": "postFulfillmentStatusSpecification",
        },
    )
    class FulfillmentCodeHookSettingProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            fulfillment_updates_specification: typing.Optional[typing.Union["CfnBot.FulfillmentUpdatesSpecificationProperty", _IResolvable_a771d0ef]] = None,
            post_fulfillment_status_specification: typing.Optional[typing.Union["CfnBot.PostFulfillmentStatusSpecificationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnBot.FulfillmentCodeHookSettingProperty.Enabled``.
            :param fulfillment_updates_specification: ``CfnBot.FulfillmentCodeHookSettingProperty.FulfillmentUpdatesSpecification``.
            :param post_fulfillment_status_specification: ``CfnBot.FulfillmentCodeHookSettingProperty.PostFulfillmentStatusSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                fulfillment_code_hook_setting_property = lex.CfnBot.FulfillmentCodeHookSettingProperty(
                    enabled=False,
                
                    # the properties below are optional
                    fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                        active=False,
                
                        # the properties below are optional
                        start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                            delay_in_seconds=123,
                            message_groups=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        timeout_in_seconds=123,
                        update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                            frequency_in_seconds=123,
                            message_groups=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        )
                    ),
                    post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                        failure_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        success_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if fulfillment_updates_specification is not None:
                self._values["fulfillment_updates_specification"] = fulfillment_updates_specification
            if post_fulfillment_status_specification is not None:
                self._values["post_fulfillment_status_specification"] = post_fulfillment_status_specification

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnBot.FulfillmentCodeHookSettingProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def fulfillment_updates_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.FulfillmentUpdatesSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.FulfillmentCodeHookSettingProperty.FulfillmentUpdatesSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-fulfillmentupdatesspecification
            '''
            result = self._values.get("fulfillment_updates_specification")
            return typing.cast(typing.Optional[typing.Union["CfnBot.FulfillmentUpdatesSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def post_fulfillment_status_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.PostFulfillmentStatusSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.FulfillmentCodeHookSettingProperty.PostFulfillmentStatusSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-postfulfillmentstatusspecification
            '''
            result = self._values.get("post_fulfillment_status_specification")
            return typing.cast(typing.Optional[typing.Union["CfnBot.PostFulfillmentStatusSpecificationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentCodeHookSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.FulfillmentStartResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "delay_in_seconds": "delayInSeconds",
            "message_groups": "messageGroups",
        },
    )
    class FulfillmentStartResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            delay_in_seconds: jsii.Number,
            message_groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param allow_interrupt: ``CfnBot.FulfillmentStartResponseSpecificationProperty.AllowInterrupt``.
            :param delay_in_seconds: ``CfnBot.FulfillmentStartResponseSpecificationProperty.DelayInSeconds``.
            :param message_groups: ``CfnBot.FulfillmentStartResponseSpecificationProperty.MessageGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                fulfillment_start_response_specification_property = lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                    delay_in_seconds=123,
                    message_groups=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "delay_in_seconds": delay_in_seconds,
                "message_groups": message_groups,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.FulfillmentStartResponseSpecificationProperty.AllowInterrupt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def delay_in_seconds(self) -> jsii.Number:
            '''``CfnBot.FulfillmentStartResponseSpecificationProperty.DelayInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-delayinseconds
            '''
            result = self._values.get("delay_in_seconds")
            assert result is not None, "Required property 'delay_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBot.FulfillmentStartResponseSpecificationProperty.MessageGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-messagegroups
            '''
            result = self._values.get("message_groups")
            assert result is not None, "Required property 'message_groups' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentStartResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "frequency_in_seconds": "frequencyInSeconds",
            "message_groups": "messageGroups",
        },
    )
    class FulfillmentUpdateResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            frequency_in_seconds: jsii.Number,
            message_groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param allow_interrupt: ``CfnBot.FulfillmentUpdateResponseSpecificationProperty.AllowInterrupt``.
            :param frequency_in_seconds: ``CfnBot.FulfillmentUpdateResponseSpecificationProperty.FrequencyInSeconds``.
            :param message_groups: ``CfnBot.FulfillmentUpdateResponseSpecificationProperty.MessageGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                fulfillment_update_response_specification_property = lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                    frequency_in_seconds=123,
                    message_groups=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "frequency_in_seconds": frequency_in_seconds,
                "message_groups": message_groups,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.FulfillmentUpdateResponseSpecificationProperty.AllowInterrupt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def frequency_in_seconds(self) -> jsii.Number:
            '''``CfnBot.FulfillmentUpdateResponseSpecificationProperty.FrequencyInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-frequencyinseconds
            '''
            result = self._values.get("frequency_in_seconds")
            assert result is not None, "Required property 'frequency_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBot.FulfillmentUpdateResponseSpecificationProperty.MessageGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-messagegroups
            '''
            result = self._values.get("message_groups")
            assert result is not None, "Required property 'message_groups' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentUpdateResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.FulfillmentUpdatesSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active": "active",
            "start_response": "startResponse",
            "timeout_in_seconds": "timeoutInSeconds",
            "update_response": "updateResponse",
        },
    )
    class FulfillmentUpdatesSpecificationProperty:
        def __init__(
            self,
            *,
            active: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            start_response: typing.Optional[typing.Union["CfnBot.FulfillmentStartResponseSpecificationProperty", _IResolvable_a771d0ef]] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
            update_response: typing.Optional[typing.Union["CfnBot.FulfillmentUpdateResponseSpecificationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param active: ``CfnBot.FulfillmentUpdatesSpecificationProperty.Active``.
            :param start_response: ``CfnBot.FulfillmentUpdatesSpecificationProperty.StartResponse``.
            :param timeout_in_seconds: ``CfnBot.FulfillmentUpdatesSpecificationProperty.TimeoutInSeconds``.
            :param update_response: ``CfnBot.FulfillmentUpdatesSpecificationProperty.UpdateResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                fulfillment_updates_specification_property = lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                    active=False,
                
                    # the properties below are optional
                    start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                        delay_in_seconds=123,
                        message_groups=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    timeout_in_seconds=123,
                    update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                        frequency_in_seconds=123,
                        message_groups=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "active": active,
            }
            if start_response is not None:
                self._values["start_response"] = start_response
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds
            if update_response is not None:
                self._values["update_response"] = update_response

        @builtins.property
        def active(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnBot.FulfillmentUpdatesSpecificationProperty.Active``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-active
            '''
            result = self._values.get("active")
            assert result is not None, "Required property 'active' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def start_response(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.FulfillmentStartResponseSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.FulfillmentUpdatesSpecificationProperty.StartResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-startresponse
            '''
            result = self._values.get("start_response")
            return typing.cast(typing.Optional[typing.Union["CfnBot.FulfillmentStartResponseSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnBot.FulfillmentUpdatesSpecificationProperty.TimeoutInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def update_response(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.FulfillmentUpdateResponseSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.FulfillmentUpdatesSpecificationProperty.UpdateResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-updateresponse
            '''
            result = self._values.get("update_response")
            return typing.cast(typing.Optional[typing.Union["CfnBot.FulfillmentUpdateResponseSpecificationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentUpdatesSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.GrammarSlotTypeSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class GrammarSlotTypeSettingProperty:
        def __init__(
            self,
            *,
            source: typing.Optional[typing.Union["CfnBot.GrammarSlotTypeSourceProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param source: ``CfnBot.GrammarSlotTypeSettingProperty.Source``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                grammar_slot_type_setting_property = lex.CfnBot.GrammarSlotTypeSettingProperty(
                    source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                        s3_bucket_name="s3BucketName",
                        s3_object_key="s3ObjectKey",
                
                        # the properties below are optional
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.GrammarSlotTypeSourceProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.GrammarSlotTypeSettingProperty.Source``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesetting.html#cfn-lex-bot-grammarslottypesetting-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[typing.Union["CfnBot.GrammarSlotTypeSourceProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrammarSlotTypeSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.GrammarSlotTypeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_arn": "kmsKeyArn",
            "s3_bucket_name": "s3BucketName",
            "s3_object_key": "s3ObjectKey",
        },
    )
    class GrammarSlotTypeSourceProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            s3_bucket_name: builtins.str,
            s3_object_key: builtins.str,
        ) -> None:
            '''
            :param kms_key_arn: ``CfnBot.GrammarSlotTypeSourceProperty.KmsKeyArn``.
            :param s3_bucket_name: ``CfnBot.GrammarSlotTypeSourceProperty.S3BucketName``.
            :param s3_object_key: ``CfnBot.GrammarSlotTypeSourceProperty.S3ObjectKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                grammar_slot_type_source_property = lex.CfnBot.GrammarSlotTypeSourceProperty(
                    s3_bucket_name="s3BucketName",
                    s3_object_key="s3ObjectKey",
                
                    # the properties below are optional
                    kms_key_arn="kmsKeyArn"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "s3_bucket_name": s3_bucket_name,
                "s3_object_key": s3_object_key,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.GrammarSlotTypeSourceProperty.KmsKeyArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_name(self) -> builtins.str:
            '''``CfnBot.GrammarSlotTypeSourceProperty.S3BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            assert result is not None, "Required property 's3_bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_object_key(self) -> builtins.str:
            '''``CfnBot.GrammarSlotTypeSourceProperty.S3ObjectKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-s3objectkey
            '''
            result = self._values.get("s3_object_key")
            assert result is not None, "Required property 's3_object_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrammarSlotTypeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.ImageResponseCardProperty",
        jsii_struct_bases=[],
        name_mapping={
            "buttons": "buttons",
            "image_url": "imageUrl",
            "subtitle": "subtitle",
            "title": "title",
        },
    )
    class ImageResponseCardProperty:
        def __init__(
            self,
            *,
            buttons: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.ButtonProperty", _IResolvable_a771d0ef]]]] = None,
            image_url: typing.Optional[builtins.str] = None,
            subtitle: typing.Optional[builtins.str] = None,
            title: builtins.str,
        ) -> None:
            '''
            :param buttons: ``CfnBot.ImageResponseCardProperty.Buttons``.
            :param image_url: ``CfnBot.ImageResponseCardProperty.ImageUrl``.
            :param subtitle: ``CfnBot.ImageResponseCardProperty.Subtitle``.
            :param title: ``CfnBot.ImageResponseCardProperty.Title``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                image_response_card_property = lex.CfnBot.ImageResponseCardProperty(
                    title="title",
                
                    # the properties below are optional
                    buttons=[lex.CfnBot.ButtonProperty(
                        text="text",
                        value="value"
                    )],
                    image_url="imageUrl",
                    subtitle="subtitle"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "title": title,
            }
            if buttons is not None:
                self._values["buttons"] = buttons
            if image_url is not None:
                self._values["image_url"] = image_url
            if subtitle is not None:
                self._values["subtitle"] = subtitle

        @builtins.property
        def buttons(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.ButtonProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.ImageResponseCardProperty.Buttons``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-buttons
            '''
            result = self._values.get("buttons")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.ButtonProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.ImageResponseCardProperty.ImageUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subtitle(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.ImageResponseCardProperty.Subtitle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-subtitle
            '''
            result = self._values.get("subtitle")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> builtins.str:
            '''``CfnBot.ImageResponseCardProperty.Title``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-title
            '''
            result = self._values.get("title")
            assert result is not None, "Required property 'title' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageResponseCardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.InputContextProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class InputContextProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''
            :param name: ``CfnBot.InputContextProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-inputcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                input_context_property = lex.CfnBot.InputContextProperty(
                    name="name"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnBot.InputContextProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-inputcontext.html#cfn-lex-bot-inputcontext-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.IntentClosingSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"closing_response": "closingResponse", "is_active": "isActive"},
    )
    class IntentClosingSettingProperty:
        def __init__(
            self,
            *,
            closing_response: typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef],
            is_active: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param closing_response: ``CfnBot.IntentClosingSettingProperty.ClosingResponse``.
            :param is_active: ``CfnBot.IntentClosingSettingProperty.IsActive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                intent_closing_setting_property = lex.CfnBot.IntentClosingSettingProperty(
                    closing_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                
                    # the properties below are optional
                    is_active=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "closing_response": closing_response,
            }
            if is_active is not None:
                self._values["is_active"] = is_active

        @builtins.property
        def closing_response(
            self,
        ) -> typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.IntentClosingSettingProperty.ClosingResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-closingresponse
            '''
            result = self._values.get("closing_response")
            assert result is not None, "Required property 'closing_response' is missing"
            return typing.cast(typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.IntentClosingSettingProperty.IsActive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentClosingSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.IntentConfirmationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "declination_response": "declinationResponse",
            "is_active": "isActive",
            "prompt_specification": "promptSpecification",
        },
    )
    class IntentConfirmationSettingProperty:
        def __init__(
            self,
            *,
            declination_response: typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef],
            is_active: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            prompt_specification: typing.Union["CfnBot.PromptSpecificationProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param declination_response: ``CfnBot.IntentConfirmationSettingProperty.DeclinationResponse``.
            :param is_active: ``CfnBot.IntentConfirmationSettingProperty.IsActive``.
            :param prompt_specification: ``CfnBot.IntentConfirmationSettingProperty.PromptSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                intent_confirmation_setting_property = lex.CfnBot.IntentConfirmationSettingProperty(
                    declination_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        max_retries=123,
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                
                    # the properties below are optional
                    is_active=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "declination_response": declination_response,
                "prompt_specification": prompt_specification,
            }
            if is_active is not None:
                self._values["is_active"] = is_active

        @builtins.property
        def declination_response(
            self,
        ) -> typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.IntentConfirmationSettingProperty.DeclinationResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-declinationresponse
            '''
            result = self._values.get("declination_response")
            assert result is not None, "Required property 'declination_response' is missing"
            return typing.cast(typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.IntentConfirmationSettingProperty.IsActive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def prompt_specification(
            self,
        ) -> typing.Union["CfnBot.PromptSpecificationProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.IntentConfirmationSettingProperty.PromptSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-promptspecification
            '''
            result = self._values.get("prompt_specification")
            assert result is not None, "Required property 'prompt_specification' is missing"
            return typing.cast(typing.Union["CfnBot.PromptSpecificationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentConfirmationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.IntentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "dialog_code_hook": "dialogCodeHook",
            "fulfillment_code_hook": "fulfillmentCodeHook",
            "input_contexts": "inputContexts",
            "intent_closing_setting": "intentClosingSetting",
            "intent_confirmation_setting": "intentConfirmationSetting",
            "kendra_configuration": "kendraConfiguration",
            "name": "name",
            "output_contexts": "outputContexts",
            "parent_intent_signature": "parentIntentSignature",
            "sample_utterances": "sampleUtterances",
            "slot_priorities": "slotPriorities",
            "slots": "slots",
        },
    )
    class IntentProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            dialog_code_hook: typing.Optional[typing.Union["CfnBot.DialogCodeHookSettingProperty", _IResolvable_a771d0ef]] = None,
            fulfillment_code_hook: typing.Optional[typing.Union["CfnBot.FulfillmentCodeHookSettingProperty", _IResolvable_a771d0ef]] = None,
            input_contexts: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.InputContextProperty", _IResolvable_a771d0ef]]]] = None,
            intent_closing_setting: typing.Optional[typing.Union["CfnBot.IntentClosingSettingProperty", _IResolvable_a771d0ef]] = None,
            intent_confirmation_setting: typing.Optional[typing.Union["CfnBot.IntentConfirmationSettingProperty", _IResolvable_a771d0ef]] = None,
            kendra_configuration: typing.Optional[typing.Union["CfnBot.KendraConfigurationProperty", _IResolvable_a771d0ef]] = None,
            name: builtins.str,
            output_contexts: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.OutputContextProperty", _IResolvable_a771d0ef]]]] = None,
            parent_intent_signature: typing.Optional[builtins.str] = None,
            sample_utterances: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SampleUtteranceProperty", _IResolvable_a771d0ef]]]] = None,
            slot_priorities: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SlotPriorityProperty", _IResolvable_a771d0ef]]]] = None,
            slots: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SlotProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param description: ``CfnBot.IntentProperty.Description``.
            :param dialog_code_hook: ``CfnBot.IntentProperty.DialogCodeHook``.
            :param fulfillment_code_hook: ``CfnBot.IntentProperty.FulfillmentCodeHook``.
            :param input_contexts: ``CfnBot.IntentProperty.InputContexts``.
            :param intent_closing_setting: ``CfnBot.IntentProperty.IntentClosingSetting``.
            :param intent_confirmation_setting: ``CfnBot.IntentProperty.IntentConfirmationSetting``.
            :param kendra_configuration: ``CfnBot.IntentProperty.KendraConfiguration``.
            :param name: ``CfnBot.IntentProperty.Name``.
            :param output_contexts: ``CfnBot.IntentProperty.OutputContexts``.
            :param parent_intent_signature: ``CfnBot.IntentProperty.ParentIntentSignature``.
            :param sample_utterances: ``CfnBot.IntentProperty.SampleUtterances``.
            :param slot_priorities: ``CfnBot.IntentProperty.SlotPriorities``.
            :param slots: ``CfnBot.IntentProperty.Slots``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                intent_property = lex.CfnBot.IntentProperty(
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                        enabled=False
                    ),
                    fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                        enabled=False,
                
                        # the properties below are optional
                        fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                            active=False,
                
                            # the properties below are optional
                            start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                delay_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_in_seconds=123,
                            update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                frequency_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        ),
                        post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                            failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            success_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        )
                    ),
                    input_contexts=[lex.CfnBot.InputContextProperty(
                        name="name"
                    )],
                    intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                        closing_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                
                        # the properties below are optional
                        is_active=False
                    ),
                    intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                        declination_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            max_retries=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                
                        # the properties below are optional
                        is_active=False
                    ),
                    kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                        kendra_index="kendraIndex",
                
                        # the properties below are optional
                        query_filter_string="queryFilterString",
                        query_filter_string_enabled=False
                    ),
                    output_contexts=[lex.CfnBot.OutputContextProperty(
                        name="name",
                        time_to_live_in_seconds=123,
                        turns_to_live=123
                    )],
                    parent_intent_signature="parentIntentSignature",
                    sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                        utterance="utterance"
                    )],
                    slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                        priority=123,
                        slot_name="slotName"
                    )],
                    slots=[lex.CfnBot.SlotProperty(
                        name="name",
                        slot_type_name="slotTypeName",
                        value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                            slot_constraint="slotConstraint",
                
                            # the properties below are optional
                            default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                    default_value="defaultValue"
                                )]
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                utterance="utterance"
                            )],
                            wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                
                                # the properties below are optional
                                is_active=False,
                                still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                                    timeout_in_seconds=123,
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
                
                        # the properties below are optional
                        description="description",
                        multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                            allow_multiple_values=False
                        ),
                        obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                            obfuscation_setting_type="obfuscationSettingType"
                        )
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if dialog_code_hook is not None:
                self._values["dialog_code_hook"] = dialog_code_hook
            if fulfillment_code_hook is not None:
                self._values["fulfillment_code_hook"] = fulfillment_code_hook
            if input_contexts is not None:
                self._values["input_contexts"] = input_contexts
            if intent_closing_setting is not None:
                self._values["intent_closing_setting"] = intent_closing_setting
            if intent_confirmation_setting is not None:
                self._values["intent_confirmation_setting"] = intent_confirmation_setting
            if kendra_configuration is not None:
                self._values["kendra_configuration"] = kendra_configuration
            if output_contexts is not None:
                self._values["output_contexts"] = output_contexts
            if parent_intent_signature is not None:
                self._values["parent_intent_signature"] = parent_intent_signature
            if sample_utterances is not None:
                self._values["sample_utterances"] = sample_utterances
            if slot_priorities is not None:
                self._values["slot_priorities"] = slot_priorities
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.IntentProperty.Description``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dialog_code_hook(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.DialogCodeHookSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.IntentProperty.DialogCodeHook``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-dialogcodehook
            '''
            result = self._values.get("dialog_code_hook")
            return typing.cast(typing.Optional[typing.Union["CfnBot.DialogCodeHookSettingProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def fulfillment_code_hook(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.FulfillmentCodeHookSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.IntentProperty.FulfillmentCodeHook``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-fulfillmentcodehook
            '''
            result = self._values.get("fulfillment_code_hook")
            return typing.cast(typing.Optional[typing.Union["CfnBot.FulfillmentCodeHookSettingProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def input_contexts(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.InputContextProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.IntentProperty.InputContexts``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-inputcontexts
            '''
            result = self._values.get("input_contexts")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.InputContextProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def intent_closing_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.IntentClosingSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.IntentProperty.IntentClosingSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-intentclosingsetting
            '''
            result = self._values.get("intent_closing_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBot.IntentClosingSettingProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def intent_confirmation_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.IntentConfirmationSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.IntentProperty.IntentConfirmationSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-intentconfirmationsetting
            '''
            result = self._values.get("intent_confirmation_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBot.IntentConfirmationSettingProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kendra_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.KendraConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.IntentProperty.KendraConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-kendraconfiguration
            '''
            result = self._values.get("kendra_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnBot.KendraConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnBot.IntentProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def output_contexts(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.OutputContextProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.IntentProperty.OutputContexts``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-outputcontexts
            '''
            result = self._values.get("output_contexts")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.OutputContextProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def parent_intent_signature(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.IntentProperty.ParentIntentSignature``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-parentintentsignature
            '''
            result = self._values.get("parent_intent_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sample_utterances(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SampleUtteranceProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.IntentProperty.SampleUtterances``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-sampleutterances
            '''
            result = self._values.get("sample_utterances")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SampleUtteranceProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def slot_priorities(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotPriorityProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.IntentProperty.SlotPriorities``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-slotpriorities
            '''
            result = self._values.get("slot_priorities")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotPriorityProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def slots(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.IntentProperty.Slots``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-slots
            '''
            result = self._values.get("slots")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.KendraConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kendra_index": "kendraIndex",
            "query_filter_string": "queryFilterString",
            "query_filter_string_enabled": "queryFilterStringEnabled",
        },
    )
    class KendraConfigurationProperty:
        def __init__(
            self,
            *,
            kendra_index: builtins.str,
            query_filter_string: typing.Optional[builtins.str] = None,
            query_filter_string_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param kendra_index: ``CfnBot.KendraConfigurationProperty.KendraIndex``.
            :param query_filter_string: ``CfnBot.KendraConfigurationProperty.QueryFilterString``.
            :param query_filter_string_enabled: ``CfnBot.KendraConfigurationProperty.QueryFilterStringEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                kendra_configuration_property = lex.CfnBot.KendraConfigurationProperty(
                    kendra_index="kendraIndex",
                
                    # the properties below are optional
                    query_filter_string="queryFilterString",
                    query_filter_string_enabled=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "kendra_index": kendra_index,
            }
            if query_filter_string is not None:
                self._values["query_filter_string"] = query_filter_string
            if query_filter_string_enabled is not None:
                self._values["query_filter_string_enabled"] = query_filter_string_enabled

        @builtins.property
        def kendra_index(self) -> builtins.str:
            '''``CfnBot.KendraConfigurationProperty.KendraIndex``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-kendraindex
            '''
            result = self._values.get("kendra_index")
            assert result is not None, "Required property 'kendra_index' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def query_filter_string(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.KendraConfigurationProperty.QueryFilterString``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-queryfilterstring
            '''
            result = self._values.get("query_filter_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_filter_string_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.KendraConfigurationProperty.QueryFilterStringEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-queryfilterstringenabled
            '''
            result = self._values.get("query_filter_string_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KendraConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.MessageGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"message": "message", "variations": "variations"},
    )
    class MessageGroupProperty:
        def __init__(
            self,
            *,
            message: typing.Union["CfnBot.MessageProperty", _IResolvable_a771d0ef],
            variations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.MessageProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param message: ``CfnBot.MessageGroupProperty.Message``.
            :param variations: ``CfnBot.MessageGroupProperty.Variations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                message_group_property = lex.CfnBot.MessageGroupProperty(
                    message=lex.CfnBot.MessageProperty(
                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                            value="value"
                        ),
                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                            title="title",
                
                            # the properties below are optional
                            buttons=[lex.CfnBot.ButtonProperty(
                                text="text",
                                value="value"
                            )],
                            image_url="imageUrl",
                            subtitle="subtitle"
                        ),
                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                            value="value"
                        ),
                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                            value="value"
                        )
                    ),
                
                    # the properties below are optional
                    variations=[lex.CfnBot.MessageProperty(
                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                            value="value"
                        ),
                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                            title="title",
                
                            # the properties below are optional
                            buttons=[lex.CfnBot.ButtonProperty(
                                text="text",
                                value="value"
                            )],
                            image_url="imageUrl",
                            subtitle="subtitle"
                        ),
                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                            value="value"
                        ),
                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                            value="value"
                        )
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "message": message,
            }
            if variations is not None:
                self._values["variations"] = variations

        @builtins.property
        def message(
            self,
        ) -> typing.Union["CfnBot.MessageProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.MessageGroupProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html#cfn-lex-bot-messagegroup-message
            '''
            result = self._values.get("message")
            assert result is not None, "Required property 'message' is missing"
            return typing.cast(typing.Union["CfnBot.MessageProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def variations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.MessageGroupProperty.Variations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html#cfn-lex-bot-messagegroup-variations
            '''
            result = self._values.get("variations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.MessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_payload": "customPayload",
            "image_response_card": "imageResponseCard",
            "plain_text_message": "plainTextMessage",
            "ssml_message": "ssmlMessage",
        },
    )
    class MessageProperty:
        def __init__(
            self,
            *,
            custom_payload: typing.Optional[typing.Union["CfnBot.CustomPayloadProperty", _IResolvable_a771d0ef]] = None,
            image_response_card: typing.Optional[typing.Union["CfnBot.ImageResponseCardProperty", _IResolvable_a771d0ef]] = None,
            plain_text_message: typing.Optional[typing.Union["CfnBot.PlainTextMessageProperty", _IResolvable_a771d0ef]] = None,
            ssml_message: typing.Optional[typing.Union["CfnBot.SSMLMessageProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param custom_payload: ``CfnBot.MessageProperty.CustomPayload``.
            :param image_response_card: ``CfnBot.MessageProperty.ImageResponseCard``.
            :param plain_text_message: ``CfnBot.MessageProperty.PlainTextMessage``.
            :param ssml_message: ``CfnBot.MessageProperty.SSMLMessage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                message_property = lex.CfnBot.MessageProperty(
                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                        value="value"
                    ),
                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                        title="title",
                
                        # the properties below are optional
                        buttons=[lex.CfnBot.ButtonProperty(
                            text="text",
                            value="value"
                        )],
                        image_url="imageUrl",
                        subtitle="subtitle"
                    ),
                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                        value="value"
                    ),
                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                        value="value"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if custom_payload is not None:
                self._values["custom_payload"] = custom_payload
            if image_response_card is not None:
                self._values["image_response_card"] = image_response_card
            if plain_text_message is not None:
                self._values["plain_text_message"] = plain_text_message
            if ssml_message is not None:
                self._values["ssml_message"] = ssml_message

        @builtins.property
        def custom_payload(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.CustomPayloadProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.MessageProperty.CustomPayload``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-custompayload
            '''
            result = self._values.get("custom_payload")
            return typing.cast(typing.Optional[typing.Union["CfnBot.CustomPayloadProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def image_response_card(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.ImageResponseCardProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.MessageProperty.ImageResponseCard``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-imageresponsecard
            '''
            result = self._values.get("image_response_card")
            return typing.cast(typing.Optional[typing.Union["CfnBot.ImageResponseCardProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def plain_text_message(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.PlainTextMessageProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.MessageProperty.PlainTextMessage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-plaintextmessage
            '''
            result = self._values.get("plain_text_message")
            return typing.cast(typing.Optional[typing.Union["CfnBot.PlainTextMessageProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ssml_message(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.SSMLMessageProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.MessageProperty.SSMLMessage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-ssmlmessage
            '''
            result = self._values.get("ssml_message")
            return typing.cast(typing.Optional[typing.Union["CfnBot.SSMLMessageProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.MultipleValuesSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"allow_multiple_values": "allowMultipleValues"},
    )
    class MultipleValuesSettingProperty:
        def __init__(
            self,
            *,
            allow_multiple_values: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param allow_multiple_values: ``CfnBot.MultipleValuesSettingProperty.AllowMultipleValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-multiplevaluessetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                multiple_values_setting_property = lex.CfnBot.MultipleValuesSettingProperty(
                    allow_multiple_values=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if allow_multiple_values is not None:
                self._values["allow_multiple_values"] = allow_multiple_values

        @builtins.property
        def allow_multiple_values(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.MultipleValuesSettingProperty.AllowMultipleValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-multiplevaluessetting.html#cfn-lex-bot-multiplevaluessetting-allowmultiplevalues
            '''
            result = self._values.get("allow_multiple_values")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultipleValuesSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.ObfuscationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"obfuscation_setting_type": "obfuscationSettingType"},
    )
    class ObfuscationSettingProperty:
        def __init__(self, *, obfuscation_setting_type: builtins.str) -> None:
            '''
            :param obfuscation_setting_type: ``CfnBot.ObfuscationSettingProperty.ObfuscationSettingType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-obfuscationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                obfuscation_setting_property = lex.CfnBot.ObfuscationSettingProperty(
                    obfuscation_setting_type="obfuscationSettingType"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "obfuscation_setting_type": obfuscation_setting_type,
            }

        @builtins.property
        def obfuscation_setting_type(self) -> builtins.str:
            '''``CfnBot.ObfuscationSettingProperty.ObfuscationSettingType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-obfuscationsetting.html#cfn-lex-bot-obfuscationsetting-obfuscationsettingtype
            '''
            result = self._values.get("obfuscation_setting_type")
            assert result is not None, "Required property 'obfuscation_setting_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObfuscationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.OutputContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "time_to_live_in_seconds": "timeToLiveInSeconds",
            "turns_to_live": "turnsToLive",
        },
    )
    class OutputContextProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            time_to_live_in_seconds: jsii.Number,
            turns_to_live: jsii.Number,
        ) -> None:
            '''
            :param name: ``CfnBot.OutputContextProperty.Name``.
            :param time_to_live_in_seconds: ``CfnBot.OutputContextProperty.TimeToLiveInSeconds``.
            :param turns_to_live: ``CfnBot.OutputContextProperty.TurnsToLive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                output_context_property = lex.CfnBot.OutputContextProperty(
                    name="name",
                    time_to_live_in_seconds=123,
                    turns_to_live=123
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "time_to_live_in_seconds": time_to_live_in_seconds,
                "turns_to_live": turns_to_live,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnBot.OutputContextProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time_to_live_in_seconds(self) -> jsii.Number:
            '''``CfnBot.OutputContextProperty.TimeToLiveInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-timetoliveinseconds
            '''
            result = self._values.get("time_to_live_in_seconds")
            assert result is not None, "Required property 'time_to_live_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def turns_to_live(self) -> jsii.Number:
            '''``CfnBot.OutputContextProperty.TurnsToLive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-turnstolive
            '''
            result = self._values.get("turns_to_live")
            assert result is not None, "Required property 'turns_to_live' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.PlainTextMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class PlainTextMessageProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''
            :param value: ``CfnBot.PlainTextMessageProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-plaintextmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                plain_text_message_property = lex.CfnBot.PlainTextMessageProperty(
                    value="value"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBot.PlainTextMessageProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-plaintextmessage.html#cfn-lex-bot-plaintextmessage-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlainTextMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.PostFulfillmentStatusSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_response": "failureResponse",
            "success_response": "successResponse",
            "timeout_response": "timeoutResponse",
        },
    )
    class PostFulfillmentStatusSpecificationProperty:
        def __init__(
            self,
            *,
            failure_response: typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]] = None,
            success_response: typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]] = None,
            timeout_response: typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param failure_response: ``CfnBot.PostFulfillmentStatusSpecificationProperty.FailureResponse``.
            :param success_response: ``CfnBot.PostFulfillmentStatusSpecificationProperty.SuccessResponse``.
            :param timeout_response: ``CfnBot.PostFulfillmentStatusSpecificationProperty.TimeoutResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                post_fulfillment_status_specification_property = lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                    failure_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    success_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if failure_response is not None:
                self._values["failure_response"] = failure_response
            if success_response is not None:
                self._values["success_response"] = success_response
            if timeout_response is not None:
                self._values["timeout_response"] = timeout_response

        @builtins.property
        def failure_response(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.PostFulfillmentStatusSpecificationProperty.FailureResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-failureresponse
            '''
            result = self._values.get("failure_response")
            return typing.cast(typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def success_response(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.PostFulfillmentStatusSpecificationProperty.SuccessResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-successresponse
            '''
            result = self._values.get("success_response")
            return typing.cast(typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def timeout_response(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.PostFulfillmentStatusSpecificationProperty.TimeoutResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-timeoutresponse
            '''
            result = self._values.get("timeout_response")
            return typing.cast(typing.Optional[typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PostFulfillmentStatusSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.PromptSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "max_retries": "maxRetries",
            "message_groups_list": "messageGroupsList",
        },
    )
    class PromptSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            max_retries: jsii.Number,
            message_groups_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param allow_interrupt: ``CfnBot.PromptSpecificationProperty.AllowInterrupt``.
            :param max_retries: ``CfnBot.PromptSpecificationProperty.MaxRetries``.
            :param message_groups_list: ``CfnBot.PromptSpecificationProperty.MessageGroupsList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                prompt_specification_property = lex.CfnBot.PromptSpecificationProperty(
                    max_retries=123,
                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_retries": max_retries,
                "message_groups_list": message_groups_list,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.PromptSpecificationProperty.AllowInterrupt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def max_retries(self) -> jsii.Number:
            '''``CfnBot.PromptSpecificationProperty.MaxRetries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-maxretries
            '''
            result = self._values.get("max_retries")
            assert result is not None, "Required property 'max_retries' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBot.PromptSpecificationProperty.MessageGroupsList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            assert result is not None, "Required property 'message_groups_list' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PromptSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.ResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "message_groups_list": "messageGroupsList",
        },
    )
    class ResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            message_groups_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param allow_interrupt: ``CfnBot.ResponseSpecificationProperty.AllowInterrupt``.
            :param message_groups_list: ``CfnBot.ResponseSpecificationProperty.MessageGroupsList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                response_specification_property = lex.CfnBot.ResponseSpecificationProperty(
                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "message_groups_list": message_groups_list,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.ResponseSpecificationProperty.AllowInterrupt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html#cfn-lex-bot-responsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBot.ResponseSpecificationProperty.MessageGroupsList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html#cfn-lex-bot-responsespecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            assert result is not None, "Required property 'message_groups_list' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_object_key": "s3ObjectKey",
            "s3_object_version": "s3ObjectVersion",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            s3_bucket: builtins.str,
            s3_object_key: builtins.str,
            s3_object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param s3_bucket: ``CfnBot.S3LocationProperty.S3Bucket``.
            :param s3_object_key: ``CfnBot.S3LocationProperty.S3ObjectKey``.
            :param s3_object_version: ``CfnBot.S3LocationProperty.S3ObjectVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                s3_location_property = lex.CfnBot.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_object_key="s3ObjectKey",
                
                    # the properties below are optional
                    s3_object_version="s3ObjectVersion"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_object_key": s3_object_key,
            }
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''``CfnBot.S3LocationProperty.S3Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_object_key(self) -> builtins.str:
            '''``CfnBot.S3LocationProperty.S3ObjectKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3objectkey
            '''
            result = self._values.get("s3_object_key")
            assert result is not None, "Required property 's3_object_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.S3LocationProperty.S3ObjectVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SSMLMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class SSMLMessageProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''
            :param value: ``CfnBot.SSMLMessageProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-ssmlmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                s_sMLMessage_property = lex.CfnBot.SSMLMessageProperty(
                    value="value"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBot.SSMLMessageProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-ssmlmessage.html#cfn-lex-bot-ssmlmessage-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSMLMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SampleUtteranceProperty",
        jsii_struct_bases=[],
        name_mapping={"utterance": "utterance"},
    )
    class SampleUtteranceProperty:
        def __init__(self, *, utterance: builtins.str) -> None:
            '''
            :param utterance: ``CfnBot.SampleUtteranceProperty.Utterance``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                sample_utterance_property = lex.CfnBot.SampleUtteranceProperty(
                    utterance="utterance"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "utterance": utterance,
            }

        @builtins.property
        def utterance(self) -> builtins.str:
            '''``CfnBot.SampleUtteranceProperty.Utterance``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterance.html#cfn-lex-bot-sampleutterance-utterance
            '''
            result = self._values.get("utterance")
            assert result is not None, "Required property 'utterance' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleUtteranceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SampleValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class SampleValueProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''
            :param value: ``CfnBot.SampleValueProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-samplevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                sample_value_property = lex.CfnBot.SampleValueProperty(
                    value="value"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBot.SampleValueProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-samplevalue.html#cfn-lex-bot-samplevalue-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotDefaultValueProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue"},
    )
    class SlotDefaultValueProperty:
        def __init__(self, *, default_value: builtins.str) -> None:
            '''
            :param default_value: ``CfnBot.SlotDefaultValueProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_default_value_property = lex.CfnBot.SlotDefaultValueProperty(
                    default_value="defaultValue"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "default_value": default_value,
            }

        @builtins.property
        def default_value(self) -> builtins.str:
            '''``CfnBot.SlotDefaultValueProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvalue.html#cfn-lex-bot-slotdefaultvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            assert result is not None, "Required property 'default_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotDefaultValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotDefaultValueSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value_list": "defaultValueList"},
    )
    class SlotDefaultValueSpecificationProperty:
        def __init__(
            self,
            *,
            default_value_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SlotDefaultValueProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param default_value_list: ``CfnBot.SlotDefaultValueSpecificationProperty.DefaultValueList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvaluespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_default_value_specification_property = lex.CfnBot.SlotDefaultValueSpecificationProperty(
                    default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                        default_value="defaultValue"
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "default_value_list": default_value_list,
            }

        @builtins.property
        def default_value_list(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotDefaultValueProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBot.SlotDefaultValueSpecificationProperty.DefaultValueList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvaluespecification.html#cfn-lex-bot-slotdefaultvaluespecification-defaultvaluelist
            '''
            result = self._values.get("default_value_list")
            assert result is not None, "Required property 'default_value_list' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotDefaultValueProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotDefaultValueSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotPriorityProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "slot_name": "slotName"},
    )
    class SlotPriorityProperty:
        def __init__(self, *, priority: jsii.Number, slot_name: builtins.str) -> None:
            '''
            :param priority: ``CfnBot.SlotPriorityProperty.Priority``.
            :param slot_name: ``CfnBot.SlotPriorityProperty.SlotName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_priority_property = lex.CfnBot.SlotPriorityProperty(
                    priority=123,
                    slot_name="slotName"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "priority": priority,
                "slot_name": slot_name,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            '''``CfnBot.SlotPriorityProperty.Priority``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html#cfn-lex-bot-slotpriority-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def slot_name(self) -> builtins.str:
            '''``CfnBot.SlotPriorityProperty.SlotName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html#cfn-lex-bot-slotpriority-slotname
            '''
            result = self._values.get("slot_name")
            assert result is not None, "Required property 'slot_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotPriorityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "multiple_values_setting": "multipleValuesSetting",
            "name": "name",
            "obfuscation_setting": "obfuscationSetting",
            "slot_type_name": "slotTypeName",
            "value_elicitation_setting": "valueElicitationSetting",
        },
    )
    class SlotProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            multiple_values_setting: typing.Optional[typing.Union["CfnBot.MultipleValuesSettingProperty", _IResolvable_a771d0ef]] = None,
            name: builtins.str,
            obfuscation_setting: typing.Optional[typing.Union["CfnBot.ObfuscationSettingProperty", _IResolvable_a771d0ef]] = None,
            slot_type_name: builtins.str,
            value_elicitation_setting: typing.Union["CfnBot.SlotValueElicitationSettingProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param description: ``CfnBot.SlotProperty.Description``.
            :param multiple_values_setting: ``CfnBot.SlotProperty.MultipleValuesSetting``.
            :param name: ``CfnBot.SlotProperty.Name``.
            :param obfuscation_setting: ``CfnBot.SlotProperty.ObfuscationSetting``.
            :param slot_type_name: ``CfnBot.SlotProperty.SlotTypeName``.
            :param value_elicitation_setting: ``CfnBot.SlotProperty.ValueElicitationSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_property = lex.CfnBot.SlotProperty(
                    name="name",
                    slot_type_name="slotTypeName",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="slotConstraint",
                
                        # the properties below are optional
                        default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                            default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                default_value="defaultValue"
                            )]
                        ),
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            max_retries=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                            utterance="utterance"
                        )],
                        wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                            continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                
                            # the properties below are optional
                            is_active=False,
                            still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                frequency_in_seconds=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                                timeout_in_seconds=123,
                
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        )
                    ),
                
                    # the properties below are optional
                    description="description",
                    multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                        allow_multiple_values=False
                    ),
                    obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                        obfuscation_setting_type="obfuscationSettingType"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "slot_type_name": slot_type_name,
                "value_elicitation_setting": value_elicitation_setting,
            }
            if description is not None:
                self._values["description"] = description
            if multiple_values_setting is not None:
                self._values["multiple_values_setting"] = multiple_values_setting
            if obfuscation_setting is not None:
                self._values["obfuscation_setting"] = obfuscation_setting

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.SlotProperty.Description``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multiple_values_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.MultipleValuesSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotProperty.MultipleValuesSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-multiplevaluessetting
            '''
            result = self._values.get("multiple_values_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBot.MultipleValuesSettingProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnBot.SlotProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def obfuscation_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.ObfuscationSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotProperty.ObfuscationSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-obfuscationsetting
            '''
            result = self._values.get("obfuscation_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBot.ObfuscationSettingProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def slot_type_name(self) -> builtins.str:
            '''``CfnBot.SlotProperty.SlotTypeName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-slottypename
            '''
            result = self._values.get("slot_type_name")
            assert result is not None, "Required property 'slot_type_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value_elicitation_setting(
            self,
        ) -> typing.Union["CfnBot.SlotValueElicitationSettingProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.SlotProperty.ValueElicitationSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-valueelicitationsetting
            '''
            result = self._values.get("value_elicitation_setting")
            assert result is not None, "Required property 'value_elicitation_setting' is missing"
            return typing.cast(typing.Union["CfnBot.SlotValueElicitationSettingProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "external_source_setting": "externalSourceSetting",
            "name": "name",
            "parent_slot_type_signature": "parentSlotTypeSignature",
            "slot_type_values": "slotTypeValues",
            "value_selection_setting": "valueSelectionSetting",
        },
    )
    class SlotTypeProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            external_source_setting: typing.Optional[typing.Union["CfnBot.ExternalSourceSettingProperty", _IResolvable_a771d0ef]] = None,
            name: builtins.str,
            parent_slot_type_signature: typing.Optional[builtins.str] = None,
            slot_type_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SlotTypeValueProperty", _IResolvable_a771d0ef]]]] = None,
            value_selection_setting: typing.Optional[typing.Union["CfnBot.SlotValueSelectionSettingProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param description: ``CfnBot.SlotTypeProperty.Description``.
            :param external_source_setting: ``CfnBot.SlotTypeProperty.ExternalSourceSetting``.
            :param name: ``CfnBot.SlotTypeProperty.Name``.
            :param parent_slot_type_signature: ``CfnBot.SlotTypeProperty.ParentSlotTypeSignature``.
            :param slot_type_values: ``CfnBot.SlotTypeProperty.SlotTypeValues``.
            :param value_selection_setting: ``CfnBot.SlotTypeProperty.ValueSelectionSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_type_property = lex.CfnBot.SlotTypeProperty(
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                        grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                            source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                s3_bucket_name="s3BucketName",
                                s3_object_key="s3ObjectKey",
                
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        )
                    ),
                    parent_slot_type_signature="parentSlotTypeSignature",
                    slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                        sample_value=lex.CfnBot.SampleValueProperty(
                            value="value"
                        ),
                
                        # the properties below are optional
                        synonyms=[lex.CfnBot.SampleValueProperty(
                            value="value"
                        )]
                    )],
                    value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                        resolution_strategy="resolutionStrategy",
                
                        # the properties below are optional
                        regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                            pattern="pattern"
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if external_source_setting is not None:
                self._values["external_source_setting"] = external_source_setting
            if parent_slot_type_signature is not None:
                self._values["parent_slot_type_signature"] = parent_slot_type_signature
            if slot_type_values is not None:
                self._values["slot_type_values"] = slot_type_values
            if value_selection_setting is not None:
                self._values["value_selection_setting"] = value_selection_setting

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.SlotTypeProperty.Description``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_source_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.ExternalSourceSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotTypeProperty.ExternalSourceSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-externalsourcesetting
            '''
            result = self._values.get("external_source_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBot.ExternalSourceSettingProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnBot.SlotTypeProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def parent_slot_type_signature(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.SlotTypeProperty.ParentSlotTypeSignature``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-parentslottypesignature
            '''
            result = self._values.get("parent_slot_type_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_type_values(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotTypeValueProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.SlotTypeProperty.SlotTypeValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-slottypevalues
            '''
            result = self._values.get("slot_type_values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SlotTypeValueProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def value_selection_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.SlotValueSelectionSettingProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotTypeProperty.ValueSelectionSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-valueselectionsetting
            '''
            result = self._values.get("value_selection_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBot.SlotValueSelectionSettingProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotTypeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"sample_value": "sampleValue", "synonyms": "synonyms"},
    )
    class SlotTypeValueProperty:
        def __init__(
            self,
            *,
            sample_value: typing.Union["CfnBot.SampleValueProperty", _IResolvable_a771d0ef],
            synonyms: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SampleValueProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param sample_value: ``CfnBot.SlotTypeValueProperty.SampleValue``.
            :param synonyms: ``CfnBot.SlotTypeValueProperty.Synonyms``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_type_value_property = lex.CfnBot.SlotTypeValueProperty(
                    sample_value=lex.CfnBot.SampleValueProperty(
                        value="value"
                    ),
                
                    # the properties below are optional
                    synonyms=[lex.CfnBot.SampleValueProperty(
                        value="value"
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "sample_value": sample_value,
            }
            if synonyms is not None:
                self._values["synonyms"] = synonyms

        @builtins.property
        def sample_value(
            self,
        ) -> typing.Union["CfnBot.SampleValueProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.SlotTypeValueProperty.SampleValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html#cfn-lex-bot-slottypevalue-samplevalue
            '''
            result = self._values.get("sample_value")
            assert result is not None, "Required property 'sample_value' is missing"
            return typing.cast(typing.Union["CfnBot.SampleValueProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def synonyms(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SampleValueProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.SlotTypeValueProperty.Synonyms``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html#cfn-lex-bot-slottypevalue-synonyms
            '''
            result = self._values.get("synonyms")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SampleValueProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotTypeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotValueElicitationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_value_specification": "defaultValueSpecification",
            "prompt_specification": "promptSpecification",
            "sample_utterances": "sampleUtterances",
            "slot_constraint": "slotConstraint",
            "wait_and_continue_specification": "waitAndContinueSpecification",
        },
    )
    class SlotValueElicitationSettingProperty:
        def __init__(
            self,
            *,
            default_value_specification: typing.Optional[typing.Union["CfnBot.SlotDefaultValueSpecificationProperty", _IResolvable_a771d0ef]] = None,
            prompt_specification: typing.Optional[typing.Union["CfnBot.PromptSpecificationProperty", _IResolvable_a771d0ef]] = None,
            sample_utterances: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.SampleUtteranceProperty", _IResolvable_a771d0ef]]]] = None,
            slot_constraint: builtins.str,
            wait_and_continue_specification: typing.Optional[typing.Union["CfnBot.WaitAndContinueSpecificationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param default_value_specification: ``CfnBot.SlotValueElicitationSettingProperty.DefaultValueSpecification``.
            :param prompt_specification: ``CfnBot.SlotValueElicitationSettingProperty.PromptSpecification``.
            :param sample_utterances: ``CfnBot.SlotValueElicitationSettingProperty.SampleUtterances``.
            :param slot_constraint: ``CfnBot.SlotValueElicitationSettingProperty.SlotConstraint``.
            :param wait_and_continue_specification: ``CfnBot.SlotValueElicitationSettingProperty.WaitAndContinueSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_value_elicitation_setting_property = lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="slotConstraint",
                
                    # the properties below are optional
                    default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                        default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                            default_value="defaultValue"
                        )]
                    ),
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        max_retries=123,
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                        utterance="utterance"
                    )],
                    wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                        continue_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                
                        # the properties below are optional
                        is_active=False,
                        still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                            frequency_in_seconds=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                            timeout_in_seconds=123,
                
                            # the properties below are optional
                            allow_interrupt=False
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "slot_constraint": slot_constraint,
            }
            if default_value_specification is not None:
                self._values["default_value_specification"] = default_value_specification
            if prompt_specification is not None:
                self._values["prompt_specification"] = prompt_specification
            if sample_utterances is not None:
                self._values["sample_utterances"] = sample_utterances
            if wait_and_continue_specification is not None:
                self._values["wait_and_continue_specification"] = wait_and_continue_specification

        @builtins.property
        def default_value_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.SlotDefaultValueSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotValueElicitationSettingProperty.DefaultValueSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-defaultvaluespecification
            '''
            result = self._values.get("default_value_specification")
            return typing.cast(typing.Optional[typing.Union["CfnBot.SlotDefaultValueSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def prompt_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.PromptSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotValueElicitationSettingProperty.PromptSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-promptspecification
            '''
            result = self._values.get("prompt_specification")
            return typing.cast(typing.Optional[typing.Union["CfnBot.PromptSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sample_utterances(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SampleUtteranceProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBot.SlotValueElicitationSettingProperty.SampleUtterances``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-sampleutterances
            '''
            result = self._values.get("sample_utterances")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.SampleUtteranceProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def slot_constraint(self) -> builtins.str:
            '''``CfnBot.SlotValueElicitationSettingProperty.SlotConstraint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-slotconstraint
            '''
            result = self._values.get("slot_constraint")
            assert result is not None, "Required property 'slot_constraint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def wait_and_continue_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.WaitAndContinueSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotValueElicitationSettingProperty.WaitAndContinueSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-waitandcontinuespecification
            '''
            result = self._values.get("wait_and_continue_specification")
            return typing.cast(typing.Optional[typing.Union["CfnBot.WaitAndContinueSpecificationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueElicitationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotValueRegexFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"pattern": "pattern"},
    )
    class SlotValueRegexFilterProperty:
        def __init__(self, *, pattern: builtins.str) -> None:
            '''
            :param pattern: ``CfnBot.SlotValueRegexFilterProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueregexfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_value_regex_filter_property = lex.CfnBot.SlotValueRegexFilterProperty(
                    pattern="pattern"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "pattern": pattern,
            }

        @builtins.property
        def pattern(self) -> builtins.str:
            '''``CfnBot.SlotValueRegexFilterProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueregexfilter.html#cfn-lex-bot-slotvalueregexfilter-pattern
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueRegexFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.SlotValueSelectionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "regex_filter": "regexFilter",
            "resolution_strategy": "resolutionStrategy",
        },
    )
    class SlotValueSelectionSettingProperty:
        def __init__(
            self,
            *,
            regex_filter: typing.Optional[typing.Union["CfnBot.SlotValueRegexFilterProperty", _IResolvable_a771d0ef]] = None,
            resolution_strategy: builtins.str,
        ) -> None:
            '''
            :param regex_filter: ``CfnBot.SlotValueSelectionSettingProperty.RegexFilter``.
            :param resolution_strategy: ``CfnBot.SlotValueSelectionSettingProperty.ResolutionStrategy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                slot_value_selection_setting_property = lex.CfnBot.SlotValueSelectionSettingProperty(
                    resolution_strategy="resolutionStrategy",
                
                    # the properties below are optional
                    regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                        pattern="pattern"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resolution_strategy": resolution_strategy,
            }
            if regex_filter is not None:
                self._values["regex_filter"] = regex_filter

        @builtins.property
        def regex_filter(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.SlotValueRegexFilterProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.SlotValueSelectionSettingProperty.RegexFilter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-regexfilter
            '''
            result = self._values.get("regex_filter")
            return typing.cast(typing.Optional[typing.Union["CfnBot.SlotValueRegexFilterProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def resolution_strategy(self) -> builtins.str:
            '''``CfnBot.SlotValueSelectionSettingProperty.ResolutionStrategy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-resolutionstrategy
            '''
            result = self._values.get("resolution_strategy")
            assert result is not None, "Required property 'resolution_strategy' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueSelectionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.StillWaitingResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_interrupt": "allowInterrupt",
            "frequency_in_seconds": "frequencyInSeconds",
            "message_groups_list": "messageGroupsList",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class StillWaitingResponseSpecificationProperty:
        def __init__(
            self,
            *,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            frequency_in_seconds: jsii.Number,
            message_groups_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]],
            timeout_in_seconds: jsii.Number,
        ) -> None:
            '''
            :param allow_interrupt: ``CfnBot.StillWaitingResponseSpecificationProperty.AllowInterrupt``.
            :param frequency_in_seconds: ``CfnBot.StillWaitingResponseSpecificationProperty.FrequencyInSeconds``.
            :param message_groups_list: ``CfnBot.StillWaitingResponseSpecificationProperty.MessageGroupsList``.
            :param timeout_in_seconds: ``CfnBot.StillWaitingResponseSpecificationProperty.TimeoutInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                still_waiting_response_specification_property = lex.CfnBot.StillWaitingResponseSpecificationProperty(
                    frequency_in_seconds=123,
                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                    timeout_in_seconds=123,
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "frequency_in_seconds": frequency_in_seconds,
                "message_groups_list": message_groups_list,
                "timeout_in_seconds": timeout_in_seconds,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.StillWaitingResponseSpecificationProperty.AllowInterrupt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def frequency_in_seconds(self) -> jsii.Number:
            '''``CfnBot.StillWaitingResponseSpecificationProperty.FrequencyInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-frequencyinseconds
            '''
            result = self._values.get("frequency_in_seconds")
            assert result is not None, "Required property 'frequency_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBot.StillWaitingResponseSpecificationProperty.MessageGroupsList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            assert result is not None, "Required property 'message_groups_list' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBot.MessageGroupProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def timeout_in_seconds(self) -> jsii.Number:
            '''``CfnBot.StillWaitingResponseSpecificationProperty.TimeoutInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            assert result is not None, "Required property 'timeout_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StillWaitingResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.VoiceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"voice_id": "voiceId"},
    )
    class VoiceSettingsProperty:
        def __init__(self, *, voice_id: builtins.str) -> None:
            '''
            :param voice_id: ``CfnBot.VoiceSettingsProperty.VoiceId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                voice_settings_property = lex.CfnBot.VoiceSettingsProperty(
                    voice_id="voiceId"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "voice_id": voice_id,
            }

        @builtins.property
        def voice_id(self) -> builtins.str:
            '''``CfnBot.VoiceSettingsProperty.VoiceId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html#cfn-lex-bot-voicesettings-voiceid
            '''
            result = self._values.get("voice_id")
            assert result is not None, "Required property 'voice_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VoiceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBot.WaitAndContinueSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "continue_response": "continueResponse",
            "is_active": "isActive",
            "still_waiting_response": "stillWaitingResponse",
            "waiting_response": "waitingResponse",
        },
    )
    class WaitAndContinueSpecificationProperty:
        def __init__(
            self,
            *,
            continue_response: typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef],
            is_active: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            still_waiting_response: typing.Optional[typing.Union["CfnBot.StillWaitingResponseSpecificationProperty", _IResolvable_a771d0ef]] = None,
            waiting_response: typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param continue_response: ``CfnBot.WaitAndContinueSpecificationProperty.ContinueResponse``.
            :param is_active: ``CfnBot.WaitAndContinueSpecificationProperty.IsActive``.
            :param still_waiting_response: ``CfnBot.WaitAndContinueSpecificationProperty.StillWaitingResponse``.
            :param waiting_response: ``CfnBot.WaitAndContinueSpecificationProperty.WaitingResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                wait_and_continue_specification_property = lex.CfnBot.WaitAndContinueSpecificationProperty(
                    continue_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                
                    # the properties below are optional
                    is_active=False,
                    still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                        frequency_in_seconds=123,
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                        timeout_in_seconds=123,
                
                        # the properties below are optional
                        allow_interrupt=False
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "continue_response": continue_response,
                "waiting_response": waiting_response,
            }
            if is_active is not None:
                self._values["is_active"] = is_active
            if still_waiting_response is not None:
                self._values["still_waiting_response"] = still_waiting_response

        @builtins.property
        def continue_response(
            self,
        ) -> typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.WaitAndContinueSpecificationProperty.ContinueResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-continueresponse
            '''
            result = self._values.get("continue_response")
            assert result is not None, "Required property 'continue_response' is missing"
            return typing.cast(typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBot.WaitAndContinueSpecificationProperty.IsActive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def still_waiting_response(
            self,
        ) -> typing.Optional[typing.Union["CfnBot.StillWaitingResponseSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBot.WaitAndContinueSpecificationProperty.StillWaitingResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-stillwaitingresponse
            '''
            result = self._values.get("still_waiting_response")
            return typing.cast(typing.Optional[typing.Union["CfnBot.StillWaitingResponseSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def waiting_response(
            self,
        ) -> typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef]:
            '''``CfnBot.WaitAndContinueSpecificationProperty.WaitingResponse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-waitingresponse
            '''
            result = self._values.get("waiting_response")
            assert result is not None, "Required property 'waiting_response' is missing"
            return typing.cast(typing.Union["CfnBot.ResponseSpecificationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WaitAndContinueSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnBotAlias(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lex.CfnBotAlias",
):
    '''A CloudFormation ``AWS::Lex::BotAlias``.

    :cloudformationResource: AWS::Lex::BotAlias
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_lex as lex
        
        # sentiment_analysis_settings is of type object
        
        cfn_bot_alias = lex.CfnBotAlias(self, "MyCfnBotAlias",
            bot_alias_name="botAliasName",
            bot_id="botId",
        
            # the properties below are optional
            bot_alias_locale_settings=[lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                    enabled=False,
        
                    # the properties below are optional
                    code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                        lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    )
                ),
                locale_id="localeId"
            )],
            bot_alias_tags=[CfnTag(
                key="key",
                value="value"
            )],
            bot_version="botVersion",
            conversation_log_settings=lex.CfnBotAlias.ConversationLogSettingsProperty(
                audio_log_settings=[lex.CfnBotAlias.AudioLogSettingProperty(
                    destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                        s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn",
        
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn"
                        )
                    ),
                    enabled=False
                )],
                text_log_settings=[lex.CfnBotAlias.TextLogSettingProperty(
                    destination=lex.CfnBotAlias.TextLogDestinationProperty(),
                    enabled=False
                )]
            ),
            description="description",
            sentiment_analysis_settings=sentiment_analysis_settings
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        bot_alias_locale_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBotAlias.BotAliasLocaleSettingsItemProperty", _IResolvable_a771d0ef]]]] = None,
        bot_alias_name: builtins.str,
        bot_alias_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
        bot_id: builtins.str,
        bot_version: typing.Optional[builtins.str] = None,
        conversation_log_settings: typing.Optional[typing.Union["CfnBotAlias.ConversationLogSettingsProperty", _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        sentiment_analysis_settings: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Lex::BotAlias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bot_alias_locale_settings: ``AWS::Lex::BotAlias.BotAliasLocaleSettings``.
        :param bot_alias_name: ``AWS::Lex::BotAlias.BotAliasName``.
        :param bot_alias_tags: ``AWS::Lex::BotAlias.BotAliasTags``.
        :param bot_id: ``AWS::Lex::BotAlias.BotId``.
        :param bot_version: ``AWS::Lex::BotAlias.BotVersion``.
        :param conversation_log_settings: ``AWS::Lex::BotAlias.ConversationLogSettings``.
        :param description: ``AWS::Lex::BotAlias.Description``.
        :param sentiment_analysis_settings: ``AWS::Lex::BotAlias.SentimentAnalysisSettings``.
        '''
        props = CfnBotAliasProps(
            bot_alias_locale_settings=bot_alias_locale_settings,
            bot_alias_name=bot_alias_name,
            bot_alias_tags=bot_alias_tags,
            bot_id=bot_id,
            bot_version=bot_version,
            conversation_log_settings=conversation_log_settings,
            description=description,
            sentiment_analysis_settings=sentiment_analysis_settings,
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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrBotAliasId")
    def attr_bot_alias_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: BotAliasId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBotAliasId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrBotAliasStatus")
    def attr_bot_alias_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: BotAliasStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBotAliasStatus"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botAliasLocaleSettings")
    def bot_alias_locale_settings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotAlias.BotAliasLocaleSettingsItemProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Lex::BotAlias.BotAliasLocaleSettings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliaslocalesettings
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotAlias.BotAliasLocaleSettingsItemProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "botAliasLocaleSettings"))

    @bot_alias_locale_settings.setter
    def bot_alias_locale_settings(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotAlias.BotAliasLocaleSettingsItemProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "botAliasLocaleSettings", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botAliasName")
    def bot_alias_name(self) -> builtins.str:
        '''``AWS::Lex::BotAlias.BotAliasName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliasname
        '''
        return typing.cast(builtins.str, jsii.get(self, "botAliasName"))

    @bot_alias_name.setter
    def bot_alias_name(self, value: builtins.str) -> None:
        jsii.set(self, "botAliasName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botAliasTags")
    def bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''``AWS::Lex::BotAlias.BotAliasTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliastags
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], jsii.get(self, "botAliasTags"))

    @bot_alias_tags.setter
    def bot_alias_tags(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]],
    ) -> None:
        jsii.set(self, "botAliasTags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botId")
    def bot_id(self) -> builtins.str:
        '''``AWS::Lex::BotAlias.BotId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botid
        '''
        return typing.cast(builtins.str, jsii.get(self, "botId"))

    @bot_id.setter
    def bot_id(self, value: builtins.str) -> None:
        jsii.set(self, "botId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botVersion")
    def bot_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Lex::BotAlias.BotVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "botVersion"))

    @bot_version.setter
    def bot_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "botVersion", value)

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
    @jsii.member(jsii_name="conversationLogSettings")
    def conversation_log_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnBotAlias.ConversationLogSettingsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Lex::BotAlias.ConversationLogSettings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-conversationlogsettings
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBotAlias.ConversationLogSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "conversationLogSettings"))

    @conversation_log_settings.setter
    def conversation_log_settings(
        self,
        value: typing.Optional[typing.Union["CfnBotAlias.ConversationLogSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "conversationLogSettings", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Lex::BotAlias.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sentimentAnalysisSettings")
    def sentiment_analysis_settings(self) -> typing.Any:
        '''``AWS::Lex::BotAlias.SentimentAnalysisSettings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-sentimentanalysissettings
        '''
        return typing.cast(typing.Any, jsii.get(self, "sentimentAnalysisSettings"))

    @sentiment_analysis_settings.setter
    def sentiment_analysis_settings(self, value: typing.Any) -> None:
        jsii.set(self, "sentimentAnalysisSettings", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.AudioLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket"},
    )
    class AudioLogDestinationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[typing.Union["CfnBotAlias.S3BucketLogDestinationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param s3_bucket: ``CfnBotAlias.AudioLogDestinationProperty.S3Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                audio_log_destination_property = lex.CfnBotAlias.AudioLogDestinationProperty(
                    s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                        log_prefix="logPrefix",
                        s3_bucket_arn="s3BucketArn",
                
                        # the properties below are optional
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket

        @builtins.property
        def s3_bucket(
            self,
        ) -> typing.Optional[typing.Union["CfnBotAlias.S3BucketLogDestinationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBotAlias.AudioLogDestinationProperty.S3Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologdestination.html#cfn-lex-botalias-audiologdestination-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[typing.Union["CfnBotAlias.S3BucketLogDestinationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.AudioLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class AudioLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Union["CfnBotAlias.AudioLogDestinationProperty", _IResolvable_a771d0ef],
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param destination: ``CfnBotAlias.AudioLogSettingProperty.Destination``.
            :param enabled: ``CfnBotAlias.AudioLogSettingProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                audio_log_setting_property = lex.CfnBotAlias.AudioLogSettingProperty(
                    destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                        s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn",
                
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn"
                        )
                    ),
                    enabled=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination": destination,
                "enabled": enabled,
            }

        @builtins.property
        def destination(
            self,
        ) -> typing.Union["CfnBotAlias.AudioLogDestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnBotAlias.AudioLogSettingProperty.Destination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html#cfn-lex-botalias-audiologsetting-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union["CfnBotAlias.AudioLogDestinationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnBotAlias.AudioLogSettingProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html#cfn-lex-botalias-audiologsetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_alias_locale_setting": "botAliasLocaleSetting",
            "locale_id": "localeId",
        },
    )
    class BotAliasLocaleSettingsItemProperty:
        def __init__(
            self,
            *,
            bot_alias_locale_setting: typing.Optional[typing.Union["CfnBotAlias.BotAliasLocaleSettingsProperty", _IResolvable_a771d0ef]] = None,
            locale_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bot_alias_locale_setting: ``CfnBotAlias.BotAliasLocaleSettingsItemProperty.BotAliasLocaleSetting``.
            :param locale_id: ``CfnBotAlias.BotAliasLocaleSettingsItemProperty.LocaleId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                bot_alias_locale_settings_item_property = lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                        enabled=False,
                
                        # the properties below are optional
                        code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        )
                    ),
                    locale_id="localeId"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if bot_alias_locale_setting is not None:
                self._values["bot_alias_locale_setting"] = bot_alias_locale_setting
            if locale_id is not None:
                self._values["locale_id"] = locale_id

        @builtins.property
        def bot_alias_locale_setting(
            self,
        ) -> typing.Optional[typing.Union["CfnBotAlias.BotAliasLocaleSettingsProperty", _IResolvable_a771d0ef]]:
            '''``CfnBotAlias.BotAliasLocaleSettingsItemProperty.BotAliasLocaleSetting``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html#cfn-lex-botalias-botaliaslocalesettingsitem-botaliaslocalesetting
            '''
            result = self._values.get("bot_alias_locale_setting")
            return typing.cast(typing.Optional[typing.Union["CfnBotAlias.BotAliasLocaleSettingsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def locale_id(self) -> typing.Optional[builtins.str]:
            '''``CfnBotAlias.BotAliasLocaleSettingsItemProperty.LocaleId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html#cfn-lex-botalias-botaliaslocalesettingsitem-localeid
            '''
            result = self._values.get("locale_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.BotAliasLocaleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_specification": "codeHookSpecification",
            "enabled": "enabled",
        },
    )
    class BotAliasLocaleSettingsProperty:
        def __init__(
            self,
            *,
            code_hook_specification: typing.Optional[typing.Union["CfnBotAlias.CodeHookSpecificationProperty", _IResolvable_a771d0ef]] = None,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param code_hook_specification: ``CfnBotAlias.BotAliasLocaleSettingsProperty.CodeHookSpecification``.
            :param enabled: ``CfnBotAlias.BotAliasLocaleSettingsProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                bot_alias_locale_settings_property = lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                    enabled=False,
                
                    # the properties below are optional
                    code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                        lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if code_hook_specification is not None:
                self._values["code_hook_specification"] = code_hook_specification

        @builtins.property
        def code_hook_specification(
            self,
        ) -> typing.Optional[typing.Union["CfnBotAlias.CodeHookSpecificationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBotAlias.BotAliasLocaleSettingsProperty.CodeHookSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html#cfn-lex-botalias-botaliaslocalesettings-codehookspecification
            '''
            result = self._values.get("code_hook_specification")
            return typing.cast(typing.Optional[typing.Union["CfnBotAlias.CodeHookSpecificationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnBotAlias.BotAliasLocaleSettingsProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html#cfn-lex-botalias-botaliaslocalesettings-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
            "log_prefix": "logPrefix",
        },
    )
    class CloudWatchLogGroupLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_arn: builtins.str,
            log_prefix: builtins.str,
        ) -> None:
            '''
            :param cloud_watch_log_group_arn: ``CfnBotAlias.CloudWatchLogGroupLogDestinationProperty.CloudWatchLogGroupArn``.
            :param log_prefix: ``CfnBotAlias.CloudWatchLogGroupLogDestinationProperty.LogPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                cloud_watch_log_group_log_destination_property = lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    log_prefix="logPrefix"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cloud_watch_log_group_arn": cloud_watch_log_group_arn,
                "log_prefix": log_prefix,
            }

        @builtins.property
        def cloud_watch_log_group_arn(self) -> builtins.str:
            '''``CfnBotAlias.CloudWatchLogGroupLogDestinationProperty.CloudWatchLogGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html#cfn-lex-botalias-cloudwatchloggrouplogdestination-cloudwatchloggrouparn
            '''
            result = self._values.get("cloud_watch_log_group_arn")
            assert result is not None, "Required property 'cloud_watch_log_group_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_prefix(self) -> builtins.str:
            '''``CfnBotAlias.CloudWatchLogGroupLogDestinationProperty.LogPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html#cfn-lex-botalias-cloudwatchloggrouplogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            assert result is not None, "Required property 'log_prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogGroupLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.CodeHookSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_code_hook": "lambdaCodeHook"},
    )
    class CodeHookSpecificationProperty:
        def __init__(
            self,
            *,
            lambda_code_hook: typing.Union["CfnBotAlias.LambdaCodeHookProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param lambda_code_hook: ``CfnBotAlias.CodeHookSpecificationProperty.LambdaCodeHook``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-codehookspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                code_hook_specification_property = lex.CfnBotAlias.CodeHookSpecificationProperty(
                    lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                        code_hook_interface_version="codeHookInterfaceVersion",
                        lambda_arn="lambdaArn"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "lambda_code_hook": lambda_code_hook,
            }

        @builtins.property
        def lambda_code_hook(
            self,
        ) -> typing.Union["CfnBotAlias.LambdaCodeHookProperty", _IResolvable_a771d0ef]:
            '''``CfnBotAlias.CodeHookSpecificationProperty.LambdaCodeHook``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-codehookspecification.html#cfn-lex-botalias-codehookspecification-lambdacodehook
            '''
            result = self._values.get("lambda_code_hook")
            assert result is not None, "Required property 'lambda_code_hook' is missing"
            return typing.cast(typing.Union["CfnBotAlias.LambdaCodeHookProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeHookSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.ConversationLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_log_settings": "audioLogSettings",
            "text_log_settings": "textLogSettings",
        },
    )
    class ConversationLogSettingsProperty:
        def __init__(
            self,
            *,
            audio_log_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBotAlias.AudioLogSettingProperty", _IResolvable_a771d0ef]]]] = None,
            text_log_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBotAlias.TextLogSettingProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param audio_log_settings: ``CfnBotAlias.ConversationLogSettingsProperty.AudioLogSettings``.
            :param text_log_settings: ``CfnBotAlias.ConversationLogSettingsProperty.TextLogSettings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                conversation_log_settings_property = lex.CfnBotAlias.ConversationLogSettingsProperty(
                    audio_log_settings=[lex.CfnBotAlias.AudioLogSettingProperty(
                        destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                            s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn",
                
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex.CfnBotAlias.TextLogSettingProperty(
                        destination=lex.CfnBotAlias.TextLogDestinationProperty(),
                        enabled=False
                    )]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if audio_log_settings is not None:
                self._values["audio_log_settings"] = audio_log_settings
            if text_log_settings is not None:
                self._values["text_log_settings"] = text_log_settings

        @builtins.property
        def audio_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotAlias.AudioLogSettingProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBotAlias.ConversationLogSettingsProperty.AudioLogSettings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html#cfn-lex-botalias-conversationlogsettings-audiologsettings
            '''
            result = self._values.get("audio_log_settings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotAlias.AudioLogSettingProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def text_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotAlias.TextLogSettingProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBotAlias.ConversationLogSettingsProperty.TextLogSettings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html#cfn-lex-botalias-conversationlogsettings-textlogsettings
            '''
            result = self._values.get("text_log_settings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotAlias.TextLogSettingProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConversationLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.LambdaCodeHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_interface_version": "codeHookInterfaceVersion",
            "lambda_arn": "lambdaArn",
        },
    )
    class LambdaCodeHookProperty:
        def __init__(
            self,
            *,
            code_hook_interface_version: builtins.str,
            lambda_arn: builtins.str,
        ) -> None:
            '''
            :param code_hook_interface_version: ``CfnBotAlias.LambdaCodeHookProperty.CodeHookInterfaceVersion``.
            :param lambda_arn: ``CfnBotAlias.LambdaCodeHookProperty.LambdaArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                lambda_code_hook_property = lex.CfnBotAlias.LambdaCodeHookProperty(
                    code_hook_interface_version="codeHookInterfaceVersion",
                    lambda_arn="lambdaArn"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "code_hook_interface_version": code_hook_interface_version,
                "lambda_arn": lambda_arn,
            }

        @builtins.property
        def code_hook_interface_version(self) -> builtins.str:
            '''``CfnBotAlias.LambdaCodeHookProperty.CodeHookInterfaceVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html#cfn-lex-botalias-lambdacodehook-codehookinterfaceversion
            '''
            result = self._values.get("code_hook_interface_version")
            assert result is not None, "Required property 'code_hook_interface_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def lambda_arn(self) -> builtins.str:
            '''``CfnBotAlias.LambdaCodeHookProperty.LambdaArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html#cfn-lex-botalias-lambdacodehook-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            assert result is not None, "Required property 'lambda_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaCodeHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.S3BucketLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_arn": "kmsKeyArn",
            "log_prefix": "logPrefix",
            "s3_bucket_arn": "s3BucketArn",
        },
    )
    class S3BucketLogDestinationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            log_prefix: builtins.str,
            s3_bucket_arn: builtins.str,
        ) -> None:
            '''
            :param kms_key_arn: ``CfnBotAlias.S3BucketLogDestinationProperty.KmsKeyArn``.
            :param log_prefix: ``CfnBotAlias.S3BucketLogDestinationProperty.LogPrefix``.
            :param s3_bucket_arn: ``CfnBotAlias.S3BucketLogDestinationProperty.S3BucketArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                s3_bucket_log_destination_property = lex.CfnBotAlias.S3BucketLogDestinationProperty(
                    log_prefix="logPrefix",
                    s3_bucket_arn="s3BucketArn",
                
                    # the properties below are optional
                    kms_key_arn="kmsKeyArn"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "log_prefix": log_prefix,
                "s3_bucket_arn": s3_bucket_arn,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnBotAlias.S3BucketLogDestinationProperty.KmsKeyArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_prefix(self) -> builtins.str:
            '''``CfnBotAlias.S3BucketLogDestinationProperty.LogPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            assert result is not None, "Required property 'log_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket_arn(self) -> builtins.str:
            '''``CfnBotAlias.S3BucketLogDestinationProperty.S3BucketArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-s3bucketarn
            '''
            result = self._values.get("s3_bucket_arn")
            assert result is not None, "Required property 's3_bucket_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.TextLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class TextLogDestinationProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                text_log_destination_property = lex.CfnBotAlias.TextLogDestinationProperty()
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotAlias.TextLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class TextLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union["CfnBotAlias.TextLogDestinationProperty", _IResolvable_a771d0ef]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param destination: ``CfnBotAlias.TextLogSettingProperty.Destination``.
            :param enabled: ``CfnBotAlias.TextLogSettingProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                text_log_setting_property = lex.CfnBotAlias.TextLogSettingProperty(
                    destination=lex.CfnBotAlias.TextLogDestinationProperty(),
                    enabled=False
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union["CfnBotAlias.TextLogDestinationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBotAlias.TextLogSettingProperty.Destination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html#cfn-lex-botalias-textlogsetting-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union["CfnBotAlias.TextLogDestinationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBotAlias.TextLogSettingProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html#cfn-lex-botalias-textlogsetting-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_lex.CfnBotAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "bot_alias_locale_settings": "botAliasLocaleSettings",
        "bot_alias_name": "botAliasName",
        "bot_alias_tags": "botAliasTags",
        "bot_id": "botId",
        "bot_version": "botVersion",
        "conversation_log_settings": "conversationLogSettings",
        "description": "description",
        "sentiment_analysis_settings": "sentimentAnalysisSettings",
    },
)
class CfnBotAliasProps:
    def __init__(
        self,
        *,
        bot_alias_locale_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnBotAlias.BotAliasLocaleSettingsItemProperty, _IResolvable_a771d0ef]]]] = None,
        bot_alias_name: builtins.str,
        bot_alias_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
        bot_id: builtins.str,
        bot_version: typing.Optional[builtins.str] = None,
        conversation_log_settings: typing.Optional[typing.Union[CfnBotAlias.ConversationLogSettingsProperty, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        sentiment_analysis_settings: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::Lex::BotAlias``.

        :param bot_alias_locale_settings: ``AWS::Lex::BotAlias.BotAliasLocaleSettings``.
        :param bot_alias_name: ``AWS::Lex::BotAlias.BotAliasName``.
        :param bot_alias_tags: ``AWS::Lex::BotAlias.BotAliasTags``.
        :param bot_id: ``AWS::Lex::BotAlias.BotId``.
        :param bot_version: ``AWS::Lex::BotAlias.BotVersion``.
        :param conversation_log_settings: ``AWS::Lex::BotAlias.ConversationLogSettings``.
        :param description: ``AWS::Lex::BotAlias.Description``.
        :param sentiment_analysis_settings: ``AWS::Lex::BotAlias.SentimentAnalysisSettings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_lex as lex
            
            # sentiment_analysis_settings is of type object
            
            cfn_bot_alias_props = lex.CfnBotAliasProps(
                bot_alias_name="botAliasName",
                bot_id="botId",
            
                # the properties below are optional
                bot_alias_locale_settings=[lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                        enabled=False,
            
                        # the properties below are optional
                        code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        )
                    ),
                    locale_id="localeId"
                )],
                bot_alias_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                bot_version="botVersion",
                conversation_log_settings=lex.CfnBotAlias.ConversationLogSettingsProperty(
                    audio_log_settings=[lex.CfnBotAlias.AudioLogSettingProperty(
                        destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                            s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn",
            
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex.CfnBotAlias.TextLogSettingProperty(
                        destination=lex.CfnBotAlias.TextLogDestinationProperty(),
                        enabled=False
                    )]
                ),
                description="description",
                sentiment_analysis_settings=sentiment_analysis_settings
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bot_alias_name": bot_alias_name,
            "bot_id": bot_id,
        }
        if bot_alias_locale_settings is not None:
            self._values["bot_alias_locale_settings"] = bot_alias_locale_settings
        if bot_alias_tags is not None:
            self._values["bot_alias_tags"] = bot_alias_tags
        if bot_version is not None:
            self._values["bot_version"] = bot_version
        if conversation_log_settings is not None:
            self._values["conversation_log_settings"] = conversation_log_settings
        if description is not None:
            self._values["description"] = description
        if sentiment_analysis_settings is not None:
            self._values["sentiment_analysis_settings"] = sentiment_analysis_settings

    @builtins.property
    def bot_alias_locale_settings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBotAlias.BotAliasLocaleSettingsItemProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Lex::BotAlias.BotAliasLocaleSettings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliaslocalesettings
        '''
        result = self._values.get("bot_alias_locale_settings")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBotAlias.BotAliasLocaleSettingsItemProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def bot_alias_name(self) -> builtins.str:
        '''``AWS::Lex::BotAlias.BotAliasName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliasname
        '''
        result = self._values.get("bot_alias_name")
        assert result is not None, "Required property 'bot_alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''``AWS::Lex::BotAlias.BotAliasTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliastags
        '''
        result = self._values.get("bot_alias_tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

    @builtins.property
    def bot_id(self) -> builtins.str:
        '''``AWS::Lex::BotAlias.BotId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botid
        '''
        result = self._values.get("bot_id")
        assert result is not None, "Required property 'bot_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bot_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Lex::BotAlias.BotVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botversion
        '''
        result = self._values.get("bot_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_log_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnBotAlias.ConversationLogSettingsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Lex::BotAlias.ConversationLogSettings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-conversationlogsettings
        '''
        result = self._values.get("conversation_log_settings")
        return typing.cast(typing.Optional[typing.Union[CfnBotAlias.ConversationLogSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Lex::BotAlias.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sentiment_analysis_settings(self) -> typing.Any:
        '''``AWS::Lex::BotAlias.SentimentAnalysisSettings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-sentimentanalysissettings
        '''
        result = self._values.get("sentiment_analysis_settings")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_lex.CfnBotProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_build_bot_locales": "autoBuildBotLocales",
        "bot_file_s3_location": "botFileS3Location",
        "bot_locales": "botLocales",
        "bot_tags": "botTags",
        "data_privacy": "dataPrivacy",
        "description": "description",
        "idle_session_ttl_in_seconds": "idleSessionTtlInSeconds",
        "name": "name",
        "role_arn": "roleArn",
        "test_bot_alias_tags": "testBotAliasTags",
    },
)
class CfnBotProps:
    def __init__(
        self,
        *,
        auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        bot_file_s3_location: typing.Optional[typing.Union[CfnBot.S3LocationProperty, _IResolvable_a771d0ef]] = None,
        bot_locales: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnBot.BotLocaleProperty, _IResolvable_a771d0ef]]]] = None,
        bot_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
        data_privacy: typing.Any,
        description: typing.Optional[builtins.str] = None,
        idle_session_ttl_in_seconds: jsii.Number,
        name: builtins.str,
        role_arn: builtins.str,
        test_bot_alias_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Lex::Bot``.

        :param auto_build_bot_locales: ``AWS::Lex::Bot.AutoBuildBotLocales``.
        :param bot_file_s3_location: ``AWS::Lex::Bot.BotFileS3Location``.
        :param bot_locales: ``AWS::Lex::Bot.BotLocales``.
        :param bot_tags: ``AWS::Lex::Bot.BotTags``.
        :param data_privacy: ``AWS::Lex::Bot.DataPrivacy``.
        :param description: ``AWS::Lex::Bot.Description``.
        :param idle_session_ttl_in_seconds: ``AWS::Lex::Bot.IdleSessionTTLInSeconds``.
        :param name: ``AWS::Lex::Bot.Name``.
        :param role_arn: ``AWS::Lex::Bot.RoleArn``.
        :param test_bot_alias_tags: ``AWS::Lex::Bot.TestBotAliasTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_lex as lex
            
            # data_privacy is of type object
            
            cfn_bot_props = lex.CfnBotProps(
                data_privacy=data_privacy,
                idle_session_ttl_in_seconds=123,
                name="name",
                role_arn="roleArn",
            
                # the properties below are optional
                auto_build_bot_locales=False,
                bot_file_s3_location=lex.CfnBot.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_object_key="s3ObjectKey",
            
                    # the properties below are optional
                    s3_object_version="s3ObjectVersion"
                ),
                bot_locales=[lex.CfnBot.BotLocaleProperty(
                    locale_id="localeId",
                    nlu_confidence_threshold=123,
            
                    # the properties below are optional
                    description="description",
                    intents=[lex.CfnBot.IntentProperty(
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                            enabled=False
                        ),
                        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                            enabled=False,
            
                            # the properties below are optional
                            fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                                active=False,
            
                                # the properties below are optional
                                start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                    delay_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_in_seconds=123,
                                update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            ),
                            post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                                failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                success_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
                        input_contexts=[lex.CfnBot.InputContextProperty(
                            name="name"
                        )],
                        intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                            closing_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
            
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
            
                                # the properties below are optional
                                allow_interrupt=False
                            ),
            
                            # the properties below are optional
                            is_active=False
                        ),
                        intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                            declination_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
            
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
            
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
            
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
            
                                # the properties below are optional
                                allow_interrupt=False
                            ),
            
                            # the properties below are optional
                            is_active=False
                        ),
                        kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                            kendra_index="kendraIndex",
            
                            # the properties below are optional
                            query_filter_string="queryFilterString",
                            query_filter_string_enabled=False
                        ),
                        output_contexts=[lex.CfnBot.OutputContextProperty(
                            name="name",
                            time_to_live_in_seconds=123,
                            turns_to_live=123
                        )],
                        parent_intent_signature="parentIntentSignature",
                        sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                            utterance="utterance"
                        )],
                        slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                            priority=123,
                            slot_name="slotName"
                        )],
                        slots=[lex.CfnBot.SlotProperty(
                            name="name",
                            slot_type_name="slotTypeName",
                            value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                                slot_constraint="slotConstraint",
            
                                # the properties below are optional
                                default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                    default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                        default_value="defaultValue"
                                    )]
                                ),
                                prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                    max_retries=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                    utterance="utterance"
                                )],
                                wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                    continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
            
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
            
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
                                    waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
            
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
            
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
            
                                    # the properties below are optional
                                    is_active=False,
                                    still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                        frequency_in_seconds=123,
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
            
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                                        timeout_in_seconds=123,
            
                                        # the properties below are optional
                                        allow_interrupt=False
                                    )
                                )
                            ),
            
                            # the properties below are optional
                            description="description",
                            multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                                allow_multiple_values=False
                            ),
                            obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                                obfuscation_setting_type="obfuscationSettingType"
                            )
                        )]
                    )],
                    slot_types=[lex.CfnBot.SlotTypeProperty(
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                            grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                                source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                    s3_bucket_name="s3BucketName",
                                    s3_object_key="s3ObjectKey",
            
                                    # the properties below are optional
                                    kms_key_arn="kmsKeyArn"
                                )
                            )
                        ),
                        parent_slot_type_signature="parentSlotTypeSignature",
                        slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                            sample_value=lex.CfnBot.SampleValueProperty(
                                value="value"
                            ),
            
                            # the properties below are optional
                            synonyms=[lex.CfnBot.SampleValueProperty(
                                value="value"
                            )]
                        )],
                        value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                            resolution_strategy="resolutionStrategy",
            
                            # the properties below are optional
                            regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                                pattern="pattern"
                            )
                        )
                    )],
                    voice_settings=lex.CfnBot.VoiceSettingsProperty(
                        voice_id="voiceId"
                    )
                )],
                bot_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                description="description",
                test_bot_alias_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "data_privacy": data_privacy,
            "idle_session_ttl_in_seconds": idle_session_ttl_in_seconds,
            "name": name,
            "role_arn": role_arn,
        }
        if auto_build_bot_locales is not None:
            self._values["auto_build_bot_locales"] = auto_build_bot_locales
        if bot_file_s3_location is not None:
            self._values["bot_file_s3_location"] = bot_file_s3_location
        if bot_locales is not None:
            self._values["bot_locales"] = bot_locales
        if bot_tags is not None:
            self._values["bot_tags"] = bot_tags
        if description is not None:
            self._values["description"] = description
        if test_bot_alias_tags is not None:
            self._values["test_bot_alias_tags"] = test_bot_alias_tags

    @builtins.property
    def auto_build_bot_locales(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Lex::Bot.AutoBuildBotLocales``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-autobuildbotlocales
        '''
        result = self._values.get("auto_build_bot_locales")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def bot_file_s3_location(
        self,
    ) -> typing.Optional[typing.Union[CfnBot.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Lex::Bot.BotFileS3Location``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botfiles3location
        '''
        result = self._values.get("bot_file_s3_location")
        return typing.cast(typing.Optional[typing.Union[CfnBot.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def bot_locales(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBot.BotLocaleProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Lex::Bot.BotLocales``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botlocales
        '''
        result = self._values.get("bot_locales")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBot.BotLocaleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def bot_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''``AWS::Lex::Bot.BotTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-bottags
        '''
        result = self._values.get("bot_tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

    @builtins.property
    def data_privacy(self) -> typing.Any:
        '''``AWS::Lex::Bot.DataPrivacy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-dataprivacy
        '''
        result = self._values.get("data_privacy")
        assert result is not None, "Required property 'data_privacy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Lex::Bot.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_session_ttl_in_seconds(self) -> jsii.Number:
        '''``AWS::Lex::Bot.IdleSessionTTLInSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-idlesessionttlinseconds
        '''
        result = self._values.get("idle_session_ttl_in_seconds")
        assert result is not None, "Required property 'idle_session_ttl_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Lex::Bot.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''``AWS::Lex::Bot.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def test_bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''``AWS::Lex::Bot.TestBotAliasTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliastags
        '''
        result = self._values.get("test_bot_alias_tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnBotVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lex.CfnBotVersion",
):
    '''A CloudFormation ``AWS::Lex::BotVersion``.

    :cloudformationResource: AWS::Lex::BotVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_lex as lex
        
        cfn_bot_version = lex.CfnBotVersion(self, "MyCfnBotVersion",
            bot_id="botId",
            bot_version_locale_specification=[lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                    source_bot_version="sourceBotVersion"
                ),
                locale_id="localeId"
            )],
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        bot_id: builtins.str,
        bot_version_locale_specification: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union["CfnBotVersion.BotVersionLocaleSpecificationProperty", _IResolvable_a771d0ef]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Lex::BotVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bot_id: ``AWS::Lex::BotVersion.BotId``.
        :param bot_version_locale_specification: ``AWS::Lex::BotVersion.BotVersionLocaleSpecification``.
        :param description: ``AWS::Lex::BotVersion.Description``.
        '''
        props = CfnBotVersionProps(
            bot_id=bot_id,
            bot_version_locale_specification=bot_version_locale_specification,
            description=description,
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
    @jsii.member(jsii_name="attrBotVersion")
    def attr_bot_version(self) -> builtins.str:
        '''
        :cloudformationAttribute: BotVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBotVersion"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botId")
    def bot_id(self) -> builtins.str:
        '''``AWS::Lex::BotVersion.BotId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botid
        '''
        return typing.cast(builtins.str, jsii.get(self, "botId"))

    @bot_id.setter
    def bot_id(self, value: builtins.str) -> None:
        jsii.set(self, "botId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="botVersionLocaleSpecification")
    def bot_version_locale_specification(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotVersion.BotVersionLocaleSpecificationProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::Lex::BotVersion.BotVersionLocaleSpecification``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botversionlocalespecification
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotVersion.BotVersionLocaleSpecificationProperty", _IResolvable_a771d0ef]]], jsii.get(self, "botVersionLocaleSpecification"))

    @bot_version_locale_specification.setter
    def bot_version_locale_specification(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBotVersion.BotVersionLocaleSpecificationProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "botVersionLocaleSpecification", value)

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
        '''``AWS::Lex::BotVersion.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotVersion.BotVersionLocaleDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"source_bot_version": "sourceBotVersion"},
    )
    class BotVersionLocaleDetailsProperty:
        def __init__(self, *, source_bot_version: builtins.str) -> None:
            '''
            :param source_bot_version: ``CfnBotVersion.BotVersionLocaleDetailsProperty.SourceBotVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocaledetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                bot_version_locale_details_property = lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                    source_bot_version="sourceBotVersion"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "source_bot_version": source_bot_version,
            }

        @builtins.property
        def source_bot_version(self) -> builtins.str:
            '''``CfnBotVersion.BotVersionLocaleDetailsProperty.SourceBotVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocaledetails.html#cfn-lex-botversion-botversionlocaledetails-sourcebotversion
            '''
            result = self._values.get("source_bot_version")
            assert result is not None, "Required property 'source_bot_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotVersionLocaleDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnBotVersion.BotVersionLocaleSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_version_locale_details": "botVersionLocaleDetails",
            "locale_id": "localeId",
        },
    )
    class BotVersionLocaleSpecificationProperty:
        def __init__(
            self,
            *,
            bot_version_locale_details: typing.Union["CfnBotVersion.BotVersionLocaleDetailsProperty", _IResolvable_a771d0ef],
            locale_id: builtins.str,
        ) -> None:
            '''
            :param bot_version_locale_details: ``CfnBotVersion.BotVersionLocaleSpecificationProperty.BotVersionLocaleDetails``.
            :param locale_id: ``CfnBotVersion.BotVersionLocaleSpecificationProperty.LocaleId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                bot_version_locale_specification_property = lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                        source_bot_version="sourceBotVersion"
                    ),
                    locale_id="localeId"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bot_version_locale_details": bot_version_locale_details,
                "locale_id": locale_id,
            }

        @builtins.property
        def bot_version_locale_details(
            self,
        ) -> typing.Union["CfnBotVersion.BotVersionLocaleDetailsProperty", _IResolvable_a771d0ef]:
            '''``CfnBotVersion.BotVersionLocaleSpecificationProperty.BotVersionLocaleDetails``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html#cfn-lex-botversion-botversionlocalespecification-botversionlocaledetails
            '''
            result = self._values.get("bot_version_locale_details")
            assert result is not None, "Required property 'bot_version_locale_details' is missing"
            return typing.cast(typing.Union["CfnBotVersion.BotVersionLocaleDetailsProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def locale_id(self) -> builtins.str:
            '''``CfnBotVersion.BotVersionLocaleSpecificationProperty.LocaleId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html#cfn-lex-botversion-botversionlocalespecification-localeid
            '''
            result = self._values.get("locale_id")
            assert result is not None, "Required property 'locale_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotVersionLocaleSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_lex.CfnBotVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "bot_id": "botId",
        "bot_version_locale_specification": "botVersionLocaleSpecification",
        "description": "description",
    },
)
class CfnBotVersionProps:
    def __init__(
        self,
        *,
        bot_id: builtins.str,
        bot_version_locale_specification: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[CfnBotVersion.BotVersionLocaleSpecificationProperty, _IResolvable_a771d0ef]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Lex::BotVersion``.

        :param bot_id: ``AWS::Lex::BotVersion.BotId``.
        :param bot_version_locale_specification: ``AWS::Lex::BotVersion.BotVersionLocaleSpecification``.
        :param description: ``AWS::Lex::BotVersion.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_lex as lex
            
            cfn_bot_version_props = lex.CfnBotVersionProps(
                bot_id="botId",
                bot_version_locale_specification=[lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                        source_bot_version="sourceBotVersion"
                    ),
                    locale_id="localeId"
                )],
            
                # the properties below are optional
                description="description"
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bot_id": bot_id,
            "bot_version_locale_specification": bot_version_locale_specification,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def bot_id(self) -> builtins.str:
        '''``AWS::Lex::BotVersion.BotId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botid
        '''
        result = self._values.get("bot_id")
        assert result is not None, "Required property 'bot_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bot_version_locale_specification(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBotVersion.BotVersionLocaleSpecificationProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::Lex::BotVersion.BotVersionLocaleSpecification``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botversionlocalespecification
        '''
        result = self._values.get("bot_version_locale_specification")
        assert result is not None, "Required property 'bot_version_locale_specification' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBotVersion.BotVersionLocaleSpecificationProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Lex::BotVersion.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourcePolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lex.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::Lex::ResourcePolicy``.

    :cloudformationResource: AWS::Lex::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_lex as lex
        
        cfn_resource_policy = lex.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            policy=lex.CfnResourcePolicy.PolicyProperty(),
            resource_arn="resourceArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy: typing.Union["CfnResourcePolicy.PolicyProperty", _IResolvable_a771d0ef],
        resource_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Lex::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: ``AWS::Lex::ResourcePolicy.Policy``.
        :param resource_arn: ``AWS::Lex::ResourcePolicy.ResourceArn``.
        '''
        props = CfnResourcePolicyProps(policy=policy, resource_arn=resource_arn)

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrRevisionId")
    def attr_revision_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: RevisionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRevisionId"))

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
    @jsii.member(jsii_name="policy")
    def policy(
        self,
    ) -> typing.Union["CfnResourcePolicy.PolicyProperty", _IResolvable_a771d0ef]:
        '''``AWS::Lex::ResourcePolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-policy
        '''
        return typing.cast(typing.Union["CfnResourcePolicy.PolicyProperty", _IResolvable_a771d0ef], jsii.get(self, "policy"))

    @policy.setter
    def policy(
        self,
        value: typing.Union["CfnResourcePolicy.PolicyProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "policy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''``AWS::Lex::ResourcePolicy.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-resourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        jsii.set(self, "resourceArn", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_lex.CfnResourcePolicy.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class PolicyProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-resourcepolicy-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_lex as lex
                
                policy_property = lex.CfnResourcePolicy.PolicyProperty()
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_lex.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyProps:
    def __init__(
        self,
        *,
        policy: typing.Union[CfnResourcePolicy.PolicyProperty, _IResolvable_a771d0ef],
        resource_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``AWS::Lex::ResourcePolicy``.

        :param policy: ``AWS::Lex::ResourcePolicy.Policy``.
        :param resource_arn: ``AWS::Lex::ResourcePolicy.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_lex as lex
            
            cfn_resource_policy_props = lex.CfnResourcePolicyProps(
                policy=lex.CfnResourcePolicy.PolicyProperty(),
                resource_arn="resourceArn"
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "policy": policy,
            "resource_arn": resource_arn,
        }

    @builtins.property
    def policy(
        self,
    ) -> typing.Union[CfnResourcePolicy.PolicyProperty, _IResolvable_a771d0ef]:
        '''``AWS::Lex::ResourcePolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Union[CfnResourcePolicy.PolicyProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''``AWS::Lex::ResourcePolicy.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnBot",
    "CfnBotAlias",
    "CfnBotAliasProps",
    "CfnBotProps",
    "CfnBotVersion",
    "CfnBotVersionProps",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
]

publication.publish()
