# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from akeyless.configuration import Configuration


class ManagedKeyTargetInfo(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'external_kms_id': 'ExternalKMSKeyId',
        'key_purpose': 'list[str]',
        'key_statuses': 'list[ManagedKeyStatusInfo]',
        'target_assoc_id': 'str'
    }

    attribute_map = {
        'external_kms_id': 'external_kms_id',
        'key_purpose': 'key_purpose',
        'key_statuses': 'key_statuses',
        'target_assoc_id': 'target_assoc_id'
    }

    def __init__(self, external_kms_id=None, key_purpose=None, key_statuses=None, target_assoc_id=None, local_vars_configuration=None):  # noqa: E501
        """ManagedKeyTargetInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._external_kms_id = None
        self._key_purpose = None
        self._key_statuses = None
        self._target_assoc_id = None
        self.discriminator = None

        if external_kms_id is not None:
            self.external_kms_id = external_kms_id
        if key_purpose is not None:
            self.key_purpose = key_purpose
        if key_statuses is not None:
            self.key_statuses = key_statuses
        if target_assoc_id is not None:
            self.target_assoc_id = target_assoc_id

    @property
    def external_kms_id(self):
        """Gets the external_kms_id of this ManagedKeyTargetInfo.  # noqa: E501


        :return: The external_kms_id of this ManagedKeyTargetInfo.  # noqa: E501
        :rtype: ExternalKMSKeyId
        """
        return self._external_kms_id

    @external_kms_id.setter
    def external_kms_id(self, external_kms_id):
        """Sets the external_kms_id of this ManagedKeyTargetInfo.


        :param external_kms_id: The external_kms_id of this ManagedKeyTargetInfo.  # noqa: E501
        :type: ExternalKMSKeyId
        """

        self._external_kms_id = external_kms_id

    @property
    def key_purpose(self):
        """Gets the key_purpose of this ManagedKeyTargetInfo.  # noqa: E501


        :return: The key_purpose of this ManagedKeyTargetInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._key_purpose

    @key_purpose.setter
    def key_purpose(self, key_purpose):
        """Sets the key_purpose of this ManagedKeyTargetInfo.


        :param key_purpose: The key_purpose of this ManagedKeyTargetInfo.  # noqa: E501
        :type: list[str]
        """

        self._key_purpose = key_purpose

    @property
    def key_statuses(self):
        """Gets the key_statuses of this ManagedKeyTargetInfo.  # noqa: E501


        :return: The key_statuses of this ManagedKeyTargetInfo.  # noqa: E501
        :rtype: list[ManagedKeyStatusInfo]
        """
        return self._key_statuses

    @key_statuses.setter
    def key_statuses(self, key_statuses):
        """Sets the key_statuses of this ManagedKeyTargetInfo.


        :param key_statuses: The key_statuses of this ManagedKeyTargetInfo.  # noqa: E501
        :type: list[ManagedKeyStatusInfo]
        """

        self._key_statuses = key_statuses

    @property
    def target_assoc_id(self):
        """Gets the target_assoc_id of this ManagedKeyTargetInfo.  # noqa: E501


        :return: The target_assoc_id of this ManagedKeyTargetInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_assoc_id

    @target_assoc_id.setter
    def target_assoc_id(self, target_assoc_id):
        """Sets the target_assoc_id of this ManagedKeyTargetInfo.


        :param target_assoc_id: The target_assoc_id of this ManagedKeyTargetInfo.  # noqa: E501
        :type: str
        """

        self._target_assoc_id = target_assoc_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ManagedKeyTargetInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ManagedKeyTargetInfo):
            return True

        return self.to_dict() != other.to_dict()
