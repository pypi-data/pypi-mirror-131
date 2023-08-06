# type: ignore

import logging
from typing import Any, Dict, Mapping, Optional, Sequence, Union
import boto3
from mypy_boto3_sns.service_resource import (
    ServiceResourceSubscriptionsCollection,
    ServiceResourceTopicsCollection,
    Subscription,
    Topic,
    TopicSubscriptionsCollection,
)


from mypy_boto3_sns.type_defs import (
    MessageAttributeValueTypeDef,
    TagTypeDef,
    SetTopicAttributesInputTopicTypeDef,
)

from .isns import ITopicWrapper
from .type_defs import SmsTypes, SnsProtocolSubscribeTypes
from botocore.exceptions import ClientError
import json

logger = logging.getLogger(__name__)


class TopicWrapper(ITopicWrapper):
    def __init__(self, topic_arn: str) -> None:
        try:
            self._topic = boto3.resource("sns").Topic(topic_arn)
        except ClientError:
            logger.exception(f"Topic {topic_arn} not found.")
            raise

    @property
    def topic(self) -> Topic:
        return self._topic

    @staticmethod
    def publish_sms_message(
        phone_number: str,
        message: str,
        sms_type: SmsTypes = SmsTypes.Promotional,
    ) -> str:
        try:
            response = boto3.resource("sns").meta.client.publish(
                PhoneNumber=phone_number,
                Message=message,
                MessageAttributes={
                    "AWS.SNS.SMS.SMSType": {
                        "DataType": "String",
                        "StringValue": sms_type,
                    }
                },
            )
            message_id = response["MessageId"]
            logger.info(f"Published message to {phone_number}.")
        except ClientError:
            logger.exception(f"Couldn't publish message to {phone_number}.")
            raise
        else:
            return message_id

    def publish_message(
        self,
        message: str,
        *,
        attributes: Mapping[str, MessageAttributeValueTypeDef] = {},
        deduplication_id: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> str:
        try:
            kwargs = dict(
                filter(
                    lambda item: item[1] is not None,
                    dict(
                        MessageDeduplicationId=deduplication_id,
                        MessageGroupId=group_id,
                    ).items(),
                )
            )

            response = self.topic.publish(
                Message=message, MessageAttributes=attributes, **kwargs
            )
            message_id = response["MessageId"]
            logger.info(
                f"Published message with attributes {attributes} to topic {self.topic.arn}."
            )
        except ClientError:
            logger.exception(f"Couldn't publish message to topic {self.topic.arn}.")
            raise
        else:
            return message_id

    def publish_multi_message(
        self,
        subject: str,
        *,
        default_message: str,
        sms_message: str,
        email_message: str,
        deduplication_id: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> str:
        try:
            message = {
                "default": default_message,
                "sms": sms_message,
                "email": email_message,
            }

            kwargs = dict(
                filter(
                    lambda item: item[1] is not None,
                    dict(
                        MessageDeduplicationId=deduplication_id,
                        MessageGroupId=group_id,
                    ).items(),
                )
            )

            response = self.topic.publish(
                Message=json.dumps(message),
                Subject=subject,
                MessageStructure="json",
                **kwargs,
            )
            message_id = response["MessageId"]
            logger.info(f"Published multi-format message to topic {self.topic.arn}.")
        except ClientError:
            logger.exception(f"Couldn't publish message to topic {self.topic.arn}.")
            raise
        else:
            return message_id
