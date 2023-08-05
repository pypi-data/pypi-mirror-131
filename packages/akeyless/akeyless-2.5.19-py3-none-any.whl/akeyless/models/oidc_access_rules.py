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


class OIDCAccessRules(object):
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
        'allowed_redirect_ur_is': 'list[str]',
        'bound_claims': 'list[OIDCCustomClaim]',
        'client_id': 'str',
        'client_secret': 'str',
        'issuer': 'str',
        'unique_identifier': 'str'
    }

    attribute_map = {
        'allowed_redirect_ur_is': 'allowed_redirect_URIs',
        'bound_claims': 'bound_claims',
        'client_id': 'client_id',
        'client_secret': 'client_secret',
        'issuer': 'issuer',
        'unique_identifier': 'unique_identifier'
    }

    def __init__(self, allowed_redirect_ur_is=None, bound_claims=None, client_id=None, client_secret=None, issuer=None, unique_identifier=None, local_vars_configuration=None):  # noqa: E501
        """OIDCAccessRules - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._allowed_redirect_ur_is = None
        self._bound_claims = None
        self._client_id = None
        self._client_secret = None
        self._issuer = None
        self._unique_identifier = None
        self.discriminator = None

        if allowed_redirect_ur_is is not None:
            self.allowed_redirect_ur_is = allowed_redirect_ur_is
        if bound_claims is not None:
            self.bound_claims = bound_claims
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if issuer is not None:
            self.issuer = issuer
        if unique_identifier is not None:
            self.unique_identifier = unique_identifier

    @property
    def allowed_redirect_ur_is(self):
        """Gets the allowed_redirect_ur_is of this OIDCAccessRules.  # noqa: E501

        Allowed redirect URIs after the authentication  # noqa: E501

        :return: The allowed_redirect_ur_is of this OIDCAccessRules.  # noqa: E501
        :rtype: list[str]
        """
        return self._allowed_redirect_ur_is

    @allowed_redirect_ur_is.setter
    def allowed_redirect_ur_is(self, allowed_redirect_ur_is):
        """Sets the allowed_redirect_ur_is of this OIDCAccessRules.

        Allowed redirect URIs after the authentication  # noqa: E501

        :param allowed_redirect_ur_is: The allowed_redirect_ur_is of this OIDCAccessRules.  # noqa: E501
        :type: list[str]
        """

        self._allowed_redirect_ur_is = allowed_redirect_ur_is

    @property
    def bound_claims(self):
        """Gets the bound_claims of this OIDCAccessRules.  # noqa: E501

        The claims that login is restricted to.  # noqa: E501

        :return: The bound_claims of this OIDCAccessRules.  # noqa: E501
        :rtype: list[OIDCCustomClaim]
        """
        return self._bound_claims

    @bound_claims.setter
    def bound_claims(self, bound_claims):
        """Sets the bound_claims of this OIDCAccessRules.

        The claims that login is restricted to.  # noqa: E501

        :param bound_claims: The bound_claims of this OIDCAccessRules.  # noqa: E501
        :type: list[OIDCCustomClaim]
        """

        self._bound_claims = bound_claims

    @property
    def client_id(self):
        """Gets the client_id of this OIDCAccessRules.  # noqa: E501

        Client ID  # noqa: E501

        :return: The client_id of this OIDCAccessRules.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this OIDCAccessRules.

        Client ID  # noqa: E501

        :param client_id: The client_id of this OIDCAccessRules.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def client_secret(self):
        """Gets the client_secret of this OIDCAccessRules.  # noqa: E501

        Client Secret  # noqa: E501

        :return: The client_secret of this OIDCAccessRules.  # noqa: E501
        :rtype: str
        """
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        """Sets the client_secret of this OIDCAccessRules.

        Client Secret  # noqa: E501

        :param client_secret: The client_secret of this OIDCAccessRules.  # noqa: E501
        :type: str
        """

        self._client_secret = client_secret

    @property
    def issuer(self):
        """Gets the issuer of this OIDCAccessRules.  # noqa: E501

        Issuer URL  # noqa: E501

        :return: The issuer of this OIDCAccessRules.  # noqa: E501
        :rtype: str
        """
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        """Sets the issuer of this OIDCAccessRules.

        Issuer URL  # noqa: E501

        :param issuer: The issuer of this OIDCAccessRules.  # noqa: E501
        :type: str
        """

        self._issuer = issuer

    @property
    def unique_identifier(self):
        """Gets the unique_identifier of this OIDCAccessRules.  # noqa: E501

        A unique identifier to distinguish different users  # noqa: E501

        :return: The unique_identifier of this OIDCAccessRules.  # noqa: E501
        :rtype: str
        """
        return self._unique_identifier

    @unique_identifier.setter
    def unique_identifier(self, unique_identifier):
        """Sets the unique_identifier of this OIDCAccessRules.

        A unique identifier to distinguish different users  # noqa: E501

        :param unique_identifier: The unique_identifier of this OIDCAccessRules.  # noqa: E501
        :type: str
        """

        self._unique_identifier = unique_identifier

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
        if not isinstance(other, OIDCAccessRules):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OIDCAccessRules):
            return True

        return self.to_dict() != other.to_dict()
