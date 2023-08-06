from abc import ABC, abstractmethod
from typing import Mapping

from mypy_boto3_sns.service_resource import (
    Topic,
)
from mypy_boto3_sns.type_defs import (
    MessageAttributeValueTypeDef,
)
from .type_defs import SmsTypes


class ITopicWrapper(ABC):
    """Encapsulates Amazon SNS topic and subscription functions."""

    @abstractmethod
    def __init__(self, topic_arn: str) -> None:
        ...

    @property
    @abstractmethod
    def topic(self) -> Topic:
        ...

    @staticmethod
    @abstractmethod
    def publish_sms_message(
        phone_number: str, message: str, sms_type: SmsTypes = SmsTypes.Promotional
    ) -> str:
        """
        Publishes a text message directly to a phone number without need for a
        subscription.
        :param phone_number: The phone number that receives the message. This must be
                             in E.164 format. For example, a United States phone
                             number might be +12065550101.
        :param message: The message to send.
        :param sms_type: The sms type. "Promotional" or "Transactional"
        :return: The ID of the message.
        """

    @abstractmethod
    def publish_message(
        self,
        message: str,
        *,
        attributes: Mapping[str, MessageAttributeValueTypeDef] = {},
        deduplication_id: str = ...,
        group_id: str = ...,
    ) -> str:
        """
        Publishes a message, with attributes, to a topic. Subscriptions can be filtered
        based on message attributes so that a subscription receives messages only
        when specified attributes are present.
        :param message: The message to publish.
        :param attributes: The key-value attributes to attach to the message. Values
                           must be either `str` or `bytes`.
        :param deduplication_id: This parameter applies only to FIFO (first-in-first-out) topics.
                                 It can contain up to 128 alphanumeric characters (a-z, A-Z, 0-9)
                                 and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~).
        :param group_id: This parameter applies only to FIFO (first-in-first-out) topics.
                         The MessageGroupId can contain up to 128 alphanumeric characters (a-z, A-Z, 0-9)
                         and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~) .
        :return: The ID of the message.
        """

    @abstractmethod
    def publish_multi_message(
        self,
        subject: str,
        *,
        default_message: str,
        sms_message: str,
        email_message: str,
        deduplication_id: str = ...,
        group_id: str = ...,
    ) -> str:
        """
        Publishes a multi-format message to a topic. A multi-format message takes
        different forms based on the protocol of the subscriber. For example,
        an SMS subscriber might receive a short, text-only version of the message
        while an email subscriber could receive an HTML version of the message.
        :param subject: The subject of the message.
        :param default_message: The default version of the message. This version is
                                sent to subscribers that have protocols that are not
                                otherwise specified in the structured message.
        :param sms_message: The version of the message sent to SMS subscribers.
        :param email_message: The version of the message sent to email subscribers.
        :param deduplication_id: This parameter applies only to FIFO (first-in-first-out) topics.
                                 It can contain up to 128 alphanumeric characters (a-z, A-Z, 0-9)
                                 and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~).
        :param group_id: This parameter applies only to FIFO (first-in-first-out) topics.
                         The MessageGroupId can contain up to 128 alphanumeric characters (a-z, A-Z, 0-9)
                         and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~) .
        :return: The ID of the message.
        """
