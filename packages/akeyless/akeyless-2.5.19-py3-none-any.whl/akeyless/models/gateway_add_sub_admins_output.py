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


class GatewayAddSubAdminsOutput(object):
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
        'sub_admins': 'list[str]'
    }

    attribute_map = {
        'sub_admins': 'sub-admins'
    }

    def __init__(self, sub_admins=None, local_vars_configuration=None):  # noqa: E501
        """GatewayAddSubAdminsOutput - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._sub_admins = None
        self.discriminator = None

        if sub_admins is not None:
            self.sub_admins = sub_admins

    @property
    def sub_admins(self):
        """Gets the sub_admins of this GatewayAddSubAdminsOutput.  # noqa: E501


        :return: The sub_admins of this GatewayAddSubAdminsOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._sub_admins

    @sub_admins.setter
    def sub_admins(self, sub_admins):
        """Sets the sub_admins of this GatewayAddSubAdminsOutput.


        :param sub_admins: The sub_admins of this GatewayAddSubAdminsOutput.  # noqa: E501
        :type: list[str]
        """

        self._sub_admins = sub_admins

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
        if not isinstance(other, GatewayAddSubAdminsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayAddSubAdminsOutput):
            return True

        return self.to_dict() != other.to_dict()
