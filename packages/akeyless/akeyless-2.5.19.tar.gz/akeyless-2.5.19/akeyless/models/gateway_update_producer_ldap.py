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


class GatewayUpdateProducerLdap(object):
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
        'bind_dn': 'str',
        'bind_dn_password': 'str',
        'external_username': 'str',
        'ldap_ca_cert': 'str',
        'ldap_url': 'str',
        'name': 'str',
        'new_name': 'str',
        'password': 'str',
        'producer_encryption_key_name': 'str',
        'tags': 'list[str]',
        'target_name': 'str',
        'token': 'str',
        'token_expiration': 'str',
        'uid_token': 'str',
        'user_attribute': 'str',
        'user_dn': 'str',
        'user_ttl': 'str',
        'username': 'str'
    }

    attribute_map = {
        'bind_dn': 'bind-dn',
        'bind_dn_password': 'bind-dn-password',
        'external_username': 'external-username',
        'ldap_ca_cert': 'ldap-ca-cert',
        'ldap_url': 'ldap-url',
        'name': 'name',
        'new_name': 'new-name',
        'password': 'password',
        'producer_encryption_key_name': 'producer-encryption-key-name',
        'tags': 'tags',
        'target_name': 'target-name',
        'token': 'token',
        'token_expiration': 'token-expiration',
        'uid_token': 'uid-token',
        'user_attribute': 'user-attribute',
        'user_dn': 'user-dn',
        'user_ttl': 'user-ttl',
        'username': 'username'
    }

    def __init__(self, bind_dn=None, bind_dn_password=None, external_username='false', ldap_ca_cert=None, ldap_url=None, name=None, new_name=None, password=None, producer_encryption_key_name=None, tags=None, target_name=None, token=None, token_expiration=None, uid_token=None, user_attribute=None, user_dn=None, user_ttl='60m', username=None, local_vars_configuration=None):  # noqa: E501
        """GatewayUpdateProducerLdap - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._bind_dn = None
        self._bind_dn_password = None
        self._external_username = None
        self._ldap_ca_cert = None
        self._ldap_url = None
        self._name = None
        self._new_name = None
        self._password = None
        self._producer_encryption_key_name = None
        self._tags = None
        self._target_name = None
        self._token = None
        self._token_expiration = None
        self._uid_token = None
        self._user_attribute = None
        self._user_dn = None
        self._user_ttl = None
        self._username = None
        self.discriminator = None

        if bind_dn is not None:
            self.bind_dn = bind_dn
        if bind_dn_password is not None:
            self.bind_dn_password = bind_dn_password
        if external_username is not None:
            self.external_username = external_username
        if ldap_ca_cert is not None:
            self.ldap_ca_cert = ldap_ca_cert
        if ldap_url is not None:
            self.ldap_url = ldap_url
        self.name = name
        if new_name is not None:
            self.new_name = new_name
        if password is not None:
            self.password = password
        if producer_encryption_key_name is not None:
            self.producer_encryption_key_name = producer_encryption_key_name
        if tags is not None:
            self.tags = tags
        if target_name is not None:
            self.target_name = target_name
        if token is not None:
            self.token = token
        if token_expiration is not None:
            self.token_expiration = token_expiration
        if uid_token is not None:
            self.uid_token = uid_token
        if user_attribute is not None:
            self.user_attribute = user_attribute
        if user_dn is not None:
            self.user_dn = user_dn
        if user_ttl is not None:
            self.user_ttl = user_ttl
        if username is not None:
            self.username = username

    @property
    def bind_dn(self):
        """Gets the bind_dn of this GatewayUpdateProducerLdap.  # noqa: E501

        Bind DN  # noqa: E501

        :return: The bind_dn of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._bind_dn

    @bind_dn.setter
    def bind_dn(self, bind_dn):
        """Sets the bind_dn of this GatewayUpdateProducerLdap.

        Bind DN  # noqa: E501

        :param bind_dn: The bind_dn of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._bind_dn = bind_dn

    @property
    def bind_dn_password(self):
        """Gets the bind_dn_password of this GatewayUpdateProducerLdap.  # noqa: E501

        Bind DN Password  # noqa: E501

        :return: The bind_dn_password of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._bind_dn_password

    @bind_dn_password.setter
    def bind_dn_password(self, bind_dn_password):
        """Sets the bind_dn_password of this GatewayUpdateProducerLdap.

        Bind DN Password  # noqa: E501

        :param bind_dn_password: The bind_dn_password of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._bind_dn_password = bind_dn_password

    @property
    def external_username(self):
        """Gets the external_username of this GatewayUpdateProducerLdap.  # noqa: E501

        Fixed user  # noqa: E501

        :return: The external_username of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._external_username

    @external_username.setter
    def external_username(self, external_username):
        """Sets the external_username of this GatewayUpdateProducerLdap.

        Fixed user  # noqa: E501

        :param external_username: The external_username of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._external_username = external_username

    @property
    def ldap_ca_cert(self):
        """Gets the ldap_ca_cert of this GatewayUpdateProducerLdap.  # noqa: E501

        CA Certificate File Content  # noqa: E501

        :return: The ldap_ca_cert of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._ldap_ca_cert

    @ldap_ca_cert.setter
    def ldap_ca_cert(self, ldap_ca_cert):
        """Sets the ldap_ca_cert of this GatewayUpdateProducerLdap.

        CA Certificate File Content  # noqa: E501

        :param ldap_ca_cert: The ldap_ca_cert of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._ldap_ca_cert = ldap_ca_cert

    @property
    def ldap_url(self):
        """Gets the ldap_url of this GatewayUpdateProducerLdap.  # noqa: E501

        LDAP Server URL  # noqa: E501

        :return: The ldap_url of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._ldap_url

    @ldap_url.setter
    def ldap_url(self, ldap_url):
        """Sets the ldap_url of this GatewayUpdateProducerLdap.

        LDAP Server URL  # noqa: E501

        :param ldap_url: The ldap_url of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._ldap_url = ldap_url

    @property
    def name(self):
        """Gets the name of this GatewayUpdateProducerLdap.  # noqa: E501

        Producer name  # noqa: E501

        :return: The name of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GatewayUpdateProducerLdap.

        Producer name  # noqa: E501

        :param name: The name of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this GatewayUpdateProducerLdap.  # noqa: E501

        Producer name  # noqa: E501

        :return: The new_name of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this GatewayUpdateProducerLdap.

        Producer name  # noqa: E501

        :param new_name: The new_name of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def password(self):
        """Gets the password of this GatewayUpdateProducerLdap.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The password of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this GatewayUpdateProducerLdap.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param password: The password of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def producer_encryption_key_name(self):
        """Gets the producer_encryption_key_name of this GatewayUpdateProducerLdap.  # noqa: E501

        Dynamic producer encryption key  # noqa: E501

        :return: The producer_encryption_key_name of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._producer_encryption_key_name

    @producer_encryption_key_name.setter
    def producer_encryption_key_name(self, producer_encryption_key_name):
        """Sets the producer_encryption_key_name of this GatewayUpdateProducerLdap.

        Dynamic producer encryption key  # noqa: E501

        :param producer_encryption_key_name: The producer_encryption_key_name of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._producer_encryption_key_name = producer_encryption_key_name

    @property
    def tags(self):
        """Gets the tags of this GatewayUpdateProducerLdap.  # noqa: E501

        List of the tags attached to this secret  # noqa: E501

        :return: The tags of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this GatewayUpdateProducerLdap.

        List of the tags attached to this secret  # noqa: E501

        :param tags: The tags of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def target_name(self):
        """Gets the target_name of this GatewayUpdateProducerLdap.  # noqa: E501

        Target name  # noqa: E501

        :return: The target_name of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this GatewayUpdateProducerLdap.

        Target name  # noqa: E501

        :param target_name: The target_name of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._target_name = target_name

    @property
    def token(self):
        """Gets the token of this GatewayUpdateProducerLdap.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewayUpdateProducerLdap.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def token_expiration(self):
        """Gets the token_expiration of this GatewayUpdateProducerLdap.  # noqa: E501

        Token expiration  # noqa: E501

        :return: The token_expiration of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._token_expiration

    @token_expiration.setter
    def token_expiration(self, token_expiration):
        """Sets the token_expiration of this GatewayUpdateProducerLdap.

        Token expiration  # noqa: E501

        :param token_expiration: The token_expiration of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._token_expiration = token_expiration

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewayUpdateProducerLdap.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewayUpdateProducerLdap.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def user_attribute(self):
        """Gets the user_attribute of this GatewayUpdateProducerLdap.  # noqa: E501

        User Attribute  # noqa: E501

        :return: The user_attribute of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._user_attribute

    @user_attribute.setter
    def user_attribute(self, user_attribute):
        """Sets the user_attribute of this GatewayUpdateProducerLdap.

        User Attribute  # noqa: E501

        :param user_attribute: The user_attribute of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._user_attribute = user_attribute

    @property
    def user_dn(self):
        """Gets the user_dn of this GatewayUpdateProducerLdap.  # noqa: E501

        User DN  # noqa: E501

        :return: The user_dn of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._user_dn

    @user_dn.setter
    def user_dn(self, user_dn):
        """Sets the user_dn of this GatewayUpdateProducerLdap.

        User DN  # noqa: E501

        :param user_dn: The user_dn of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._user_dn = user_dn

    @property
    def user_ttl(self):
        """Gets the user_ttl of this GatewayUpdateProducerLdap.  # noqa: E501

        User TTL  # noqa: E501

        :return: The user_ttl of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._user_ttl

    @user_ttl.setter
    def user_ttl(self, user_ttl):
        """Sets the user_ttl of this GatewayUpdateProducerLdap.

        User TTL  # noqa: E501

        :param user_ttl: The user_ttl of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._user_ttl = user_ttl

    @property
    def username(self):
        """Gets the username of this GatewayUpdateProducerLdap.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The username of this GatewayUpdateProducerLdap.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this GatewayUpdateProducerLdap.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param username: The username of this GatewayUpdateProducerLdap.  # noqa: E501
        :type: str
        """

        self._username = username

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
        if not isinstance(other, GatewayUpdateProducerLdap):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayUpdateProducerLdap):
            return True

        return self.to_dict() != other.to_dict()
