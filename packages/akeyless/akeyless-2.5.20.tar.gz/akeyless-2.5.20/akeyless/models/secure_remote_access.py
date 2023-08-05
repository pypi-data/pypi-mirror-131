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


class SecureRemoteAccess(object):
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
        'account_id': 'str',
        'allow_port_forwarding': 'bool',
        'allow_providing_external_username': 'bool',
        'bastion_api': 'str',
        'bastion_issuer': 'str',
        'bastion_issuer_id': 'int',
        'bastion_ssh': 'str',
        'category': 'str',
        'dashboard_url': 'str',
        'db_name': 'str',
        'domain': 'str',
        'enable': 'bool',
        'endpoint': 'str',
        'host': 'list[str]',
        'is_cli': 'bool',
        'is_web': 'bool',
        'isolated': 'bool',
        'native': 'bool',
        'rdp_user': 'str',
        'region': 'str',
        'schema': 'str',
        'ssh_password': 'bool',
        'ssh_private_key': 'bool',
        'ssh_user': 'str',
        'url': 'str',
        'use_internal_bastion': 'bool'
    }

    attribute_map = {
        'account_id': 'account_id',
        'allow_port_forwarding': 'allow_port_forwarding',
        'allow_providing_external_username': 'allow_providing_external_username',
        'bastion_api': 'bastion_api',
        'bastion_issuer': 'bastion_issuer',
        'bastion_issuer_id': 'bastion_issuer_id',
        'bastion_ssh': 'bastion_ssh',
        'category': 'category',
        'dashboard_url': 'dashboard_url',
        'db_name': 'db_name',
        'domain': 'domain',
        'enable': 'enable',
        'endpoint': 'endpoint',
        'host': 'host',
        'is_cli': 'is_cli',
        'is_web': 'is_web',
        'isolated': 'isolated',
        'native': 'native',
        'rdp_user': 'rdp_user',
        'region': 'region',
        'schema': 'schema',
        'ssh_password': 'ssh_password',
        'ssh_private_key': 'ssh_private_key',
        'ssh_user': 'ssh_user',
        'url': 'url',
        'use_internal_bastion': 'use_internal_bastion'
    }

    def __init__(self, account_id=None, allow_port_forwarding=None, allow_providing_external_username=None, bastion_api=None, bastion_issuer=None, bastion_issuer_id=None, bastion_ssh=None, category=None, dashboard_url=None, db_name=None, domain=None, enable=None, endpoint=None, host=None, is_cli=None, is_web=None, isolated=None, native=None, rdp_user=None, region=None, schema=None, ssh_password=None, ssh_private_key=None, ssh_user=None, url=None, use_internal_bastion=None, local_vars_configuration=None):  # noqa: E501
        """SecureRemoteAccess - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._account_id = None
        self._allow_port_forwarding = None
        self._allow_providing_external_username = None
        self._bastion_api = None
        self._bastion_issuer = None
        self._bastion_issuer_id = None
        self._bastion_ssh = None
        self._category = None
        self._dashboard_url = None
        self._db_name = None
        self._domain = None
        self._enable = None
        self._endpoint = None
        self._host = None
        self._is_cli = None
        self._is_web = None
        self._isolated = None
        self._native = None
        self._rdp_user = None
        self._region = None
        self._schema = None
        self._ssh_password = None
        self._ssh_private_key = None
        self._ssh_user = None
        self._url = None
        self._use_internal_bastion = None
        self.discriminator = None

        if account_id is not None:
            self.account_id = account_id
        if allow_port_forwarding is not None:
            self.allow_port_forwarding = allow_port_forwarding
        if allow_providing_external_username is not None:
            self.allow_providing_external_username = allow_providing_external_username
        if bastion_api is not None:
            self.bastion_api = bastion_api
        if bastion_issuer is not None:
            self.bastion_issuer = bastion_issuer
        if bastion_issuer_id is not None:
            self.bastion_issuer_id = bastion_issuer_id
        if bastion_ssh is not None:
            self.bastion_ssh = bastion_ssh
        if category is not None:
            self.category = category
        if dashboard_url is not None:
            self.dashboard_url = dashboard_url
        if db_name is not None:
            self.db_name = db_name
        if domain is not None:
            self.domain = domain
        if enable is not None:
            self.enable = enable
        if endpoint is not None:
            self.endpoint = endpoint
        if host is not None:
            self.host = host
        if is_cli is not None:
            self.is_cli = is_cli
        if is_web is not None:
            self.is_web = is_web
        if isolated is not None:
            self.isolated = isolated
        if native is not None:
            self.native = native
        if rdp_user is not None:
            self.rdp_user = rdp_user
        if region is not None:
            self.region = region
        if schema is not None:
            self.schema = schema
        if ssh_password is not None:
            self.ssh_password = ssh_password
        if ssh_private_key is not None:
            self.ssh_private_key = ssh_private_key
        if ssh_user is not None:
            self.ssh_user = ssh_user
        if url is not None:
            self.url = url
        if use_internal_bastion is not None:
            self.use_internal_bastion = use_internal_bastion

    @property
    def account_id(self):
        """Gets the account_id of this SecureRemoteAccess.  # noqa: E501


        :return: The account_id of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this SecureRemoteAccess.


        :param account_id: The account_id of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def allow_port_forwarding(self):
        """Gets the allow_port_forwarding of this SecureRemoteAccess.  # noqa: E501


        :return: The allow_port_forwarding of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._allow_port_forwarding

    @allow_port_forwarding.setter
    def allow_port_forwarding(self, allow_port_forwarding):
        """Sets the allow_port_forwarding of this SecureRemoteAccess.


        :param allow_port_forwarding: The allow_port_forwarding of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._allow_port_forwarding = allow_port_forwarding

    @property
    def allow_providing_external_username(self):
        """Gets the allow_providing_external_username of this SecureRemoteAccess.  # noqa: E501


        :return: The allow_providing_external_username of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._allow_providing_external_username

    @allow_providing_external_username.setter
    def allow_providing_external_username(self, allow_providing_external_username):
        """Sets the allow_providing_external_username of this SecureRemoteAccess.


        :param allow_providing_external_username: The allow_providing_external_username of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._allow_providing_external_username = allow_providing_external_username

    @property
    def bastion_api(self):
        """Gets the bastion_api of this SecureRemoteAccess.  # noqa: E501


        :return: The bastion_api of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._bastion_api

    @bastion_api.setter
    def bastion_api(self, bastion_api):
        """Sets the bastion_api of this SecureRemoteAccess.


        :param bastion_api: The bastion_api of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._bastion_api = bastion_api

    @property
    def bastion_issuer(self):
        """Gets the bastion_issuer of this SecureRemoteAccess.  # noqa: E501


        :return: The bastion_issuer of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._bastion_issuer

    @bastion_issuer.setter
    def bastion_issuer(self, bastion_issuer):
        """Sets the bastion_issuer of this SecureRemoteAccess.


        :param bastion_issuer: The bastion_issuer of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._bastion_issuer = bastion_issuer

    @property
    def bastion_issuer_id(self):
        """Gets the bastion_issuer_id of this SecureRemoteAccess.  # noqa: E501


        :return: The bastion_issuer_id of this SecureRemoteAccess.  # noqa: E501
        :rtype: int
        """
        return self._bastion_issuer_id

    @bastion_issuer_id.setter
    def bastion_issuer_id(self, bastion_issuer_id):
        """Sets the bastion_issuer_id of this SecureRemoteAccess.


        :param bastion_issuer_id: The bastion_issuer_id of this SecureRemoteAccess.  # noqa: E501
        :type: int
        """

        self._bastion_issuer_id = bastion_issuer_id

    @property
    def bastion_ssh(self):
        """Gets the bastion_ssh of this SecureRemoteAccess.  # noqa: E501


        :return: The bastion_ssh of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._bastion_ssh

    @bastion_ssh.setter
    def bastion_ssh(self, bastion_ssh):
        """Sets the bastion_ssh of this SecureRemoteAccess.


        :param bastion_ssh: The bastion_ssh of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._bastion_ssh = bastion_ssh

    @property
    def category(self):
        """Gets the category of this SecureRemoteAccess.  # noqa: E501


        :return: The category of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this SecureRemoteAccess.


        :param category: The category of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def dashboard_url(self):
        """Gets the dashboard_url of this SecureRemoteAccess.  # noqa: E501


        :return: The dashboard_url of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._dashboard_url

    @dashboard_url.setter
    def dashboard_url(self, dashboard_url):
        """Sets the dashboard_url of this SecureRemoteAccess.


        :param dashboard_url: The dashboard_url of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._dashboard_url = dashboard_url

    @property
    def db_name(self):
        """Gets the db_name of this SecureRemoteAccess.  # noqa: E501


        :return: The db_name of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._db_name

    @db_name.setter
    def db_name(self, db_name):
        """Sets the db_name of this SecureRemoteAccess.


        :param db_name: The db_name of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._db_name = db_name

    @property
    def domain(self):
        """Gets the domain of this SecureRemoteAccess.  # noqa: E501


        :return: The domain of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this SecureRemoteAccess.


        :param domain: The domain of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._domain = domain

    @property
    def enable(self):
        """Gets the enable of this SecureRemoteAccess.  # noqa: E501


        :return: The enable of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._enable

    @enable.setter
    def enable(self, enable):
        """Sets the enable of this SecureRemoteAccess.


        :param enable: The enable of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._enable = enable

    @property
    def endpoint(self):
        """Gets the endpoint of this SecureRemoteAccess.  # noqa: E501


        :return: The endpoint of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """Sets the endpoint of this SecureRemoteAccess.


        :param endpoint: The endpoint of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._endpoint = endpoint

    @property
    def host(self):
        """Gets the host of this SecureRemoteAccess.  # noqa: E501


        :return: The host of this SecureRemoteAccess.  # noqa: E501
        :rtype: list[str]
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this SecureRemoteAccess.


        :param host: The host of this SecureRemoteAccess.  # noqa: E501
        :type: list[str]
        """

        self._host = host

    @property
    def is_cli(self):
        """Gets the is_cli of this SecureRemoteAccess.  # noqa: E501


        :return: The is_cli of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._is_cli

    @is_cli.setter
    def is_cli(self, is_cli):
        """Sets the is_cli of this SecureRemoteAccess.


        :param is_cli: The is_cli of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._is_cli = is_cli

    @property
    def is_web(self):
        """Gets the is_web of this SecureRemoteAccess.  # noqa: E501


        :return: The is_web of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._is_web

    @is_web.setter
    def is_web(self, is_web):
        """Sets the is_web of this SecureRemoteAccess.


        :param is_web: The is_web of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._is_web = is_web

    @property
    def isolated(self):
        """Gets the isolated of this SecureRemoteAccess.  # noqa: E501


        :return: The isolated of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._isolated

    @isolated.setter
    def isolated(self, isolated):
        """Sets the isolated of this SecureRemoteAccess.


        :param isolated: The isolated of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._isolated = isolated

    @property
    def native(self):
        """Gets the native of this SecureRemoteAccess.  # noqa: E501


        :return: The native of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._native

    @native.setter
    def native(self, native):
        """Sets the native of this SecureRemoteAccess.


        :param native: The native of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._native = native

    @property
    def rdp_user(self):
        """Gets the rdp_user of this SecureRemoteAccess.  # noqa: E501


        :return: The rdp_user of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._rdp_user

    @rdp_user.setter
    def rdp_user(self, rdp_user):
        """Sets the rdp_user of this SecureRemoteAccess.


        :param rdp_user: The rdp_user of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._rdp_user = rdp_user

    @property
    def region(self):
        """Gets the region of this SecureRemoteAccess.  # noqa: E501


        :return: The region of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this SecureRemoteAccess.


        :param region: The region of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def schema(self):
        """Gets the schema of this SecureRemoteAccess.  # noqa: E501


        :return: The schema of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """Sets the schema of this SecureRemoteAccess.


        :param schema: The schema of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._schema = schema

    @property
    def ssh_password(self):
        """Gets the ssh_password of this SecureRemoteAccess.  # noqa: E501


        :return: The ssh_password of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._ssh_password

    @ssh_password.setter
    def ssh_password(self, ssh_password):
        """Sets the ssh_password of this SecureRemoteAccess.


        :param ssh_password: The ssh_password of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._ssh_password = ssh_password

    @property
    def ssh_private_key(self):
        """Gets the ssh_private_key of this SecureRemoteAccess.  # noqa: E501


        :return: The ssh_private_key of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._ssh_private_key

    @ssh_private_key.setter
    def ssh_private_key(self, ssh_private_key):
        """Sets the ssh_private_key of this SecureRemoteAccess.


        :param ssh_private_key: The ssh_private_key of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._ssh_private_key = ssh_private_key

    @property
    def ssh_user(self):
        """Gets the ssh_user of this SecureRemoteAccess.  # noqa: E501


        :return: The ssh_user of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._ssh_user

    @ssh_user.setter
    def ssh_user(self, ssh_user):
        """Sets the ssh_user of this SecureRemoteAccess.


        :param ssh_user: The ssh_user of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._ssh_user = ssh_user

    @property
    def url(self):
        """Gets the url of this SecureRemoteAccess.  # noqa: E501


        :return: The url of this SecureRemoteAccess.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this SecureRemoteAccess.


        :param url: The url of this SecureRemoteAccess.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def use_internal_bastion(self):
        """Gets the use_internal_bastion of this SecureRemoteAccess.  # noqa: E501


        :return: The use_internal_bastion of this SecureRemoteAccess.  # noqa: E501
        :rtype: bool
        """
        return self._use_internal_bastion

    @use_internal_bastion.setter
    def use_internal_bastion(self, use_internal_bastion):
        """Sets the use_internal_bastion of this SecureRemoteAccess.


        :param use_internal_bastion: The use_internal_bastion of this SecureRemoteAccess.  # noqa: E501
        :type: bool
        """

        self._use_internal_bastion = use_internal_bastion

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
        if not isinstance(other, SecureRemoteAccess):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SecureRemoteAccess):
            return True

        return self.to_dict() != other.to_dict()
