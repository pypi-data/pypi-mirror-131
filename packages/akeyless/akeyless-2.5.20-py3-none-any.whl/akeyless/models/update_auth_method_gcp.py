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


class UpdateAuthMethodGCP(object):
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
        'access_expires': 'int',
        'audience': 'str',
        'bound_ips': 'list[str]',
        'bound_labels': 'list[str]',
        'bound_projects': 'list[str]',
        'bound_regions': 'list[str]',
        'bound_service_accounts': 'list[str]',
        'bound_zones': 'list[str]',
        'force_sub_claims': 'bool',
        'name': 'str',
        'new_name': 'str',
        'password': 'str',
        'service_account_creds_data': 'str',
        'token': 'str',
        'type': 'str',
        'uid_token': 'str',
        'username': 'str'
    }

    attribute_map = {
        'access_expires': 'access-expires',
        'audience': 'audience',
        'bound_ips': 'bound-ips',
        'bound_labels': 'bound-labels',
        'bound_projects': 'bound-projects',
        'bound_regions': 'bound-regions',
        'bound_service_accounts': 'bound-service-accounts',
        'bound_zones': 'bound-zones',
        'force_sub_claims': 'force-sub-claims',
        'name': 'name',
        'new_name': 'new-name',
        'password': 'password',
        'service_account_creds_data': 'service-account-creds-data',
        'token': 'token',
        'type': 'type',
        'uid_token': 'uid-token',
        'username': 'username'
    }

    def __init__(self, access_expires=0, audience='akeyless.io', bound_ips=None, bound_labels=None, bound_projects=None, bound_regions=None, bound_service_accounts=None, bound_zones=None, force_sub_claims=None, name=None, new_name=None, password=None, service_account_creds_data=None, token=None, type=None, uid_token=None, username=None, local_vars_configuration=None):  # noqa: E501
        """UpdateAuthMethodGCP - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._access_expires = None
        self._audience = None
        self._bound_ips = None
        self._bound_labels = None
        self._bound_projects = None
        self._bound_regions = None
        self._bound_service_accounts = None
        self._bound_zones = None
        self._force_sub_claims = None
        self._name = None
        self._new_name = None
        self._password = None
        self._service_account_creds_data = None
        self._token = None
        self._type = None
        self._uid_token = None
        self._username = None
        self.discriminator = None

        if access_expires is not None:
            self.access_expires = access_expires
        self.audience = audience
        if bound_ips is not None:
            self.bound_ips = bound_ips
        if bound_labels is not None:
            self.bound_labels = bound_labels
        if bound_projects is not None:
            self.bound_projects = bound_projects
        if bound_regions is not None:
            self.bound_regions = bound_regions
        if bound_service_accounts is not None:
            self.bound_service_accounts = bound_service_accounts
        if bound_zones is not None:
            self.bound_zones = bound_zones
        if force_sub_claims is not None:
            self.force_sub_claims = force_sub_claims
        self.name = name
        if new_name is not None:
            self.new_name = new_name
        if password is not None:
            self.password = password
        if service_account_creds_data is not None:
            self.service_account_creds_data = service_account_creds_data
        if token is not None:
            self.token = token
        self.type = type
        if uid_token is not None:
            self.uid_token = uid_token
        if username is not None:
            self.username = username

    @property
    def access_expires(self):
        """Gets the access_expires of this UpdateAuthMethodGCP.  # noqa: E501

        Access expiration date in Unix timestamp (select 0 for access without expiry date)  # noqa: E501

        :return: The access_expires of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: int
        """
        return self._access_expires

    @access_expires.setter
    def access_expires(self, access_expires):
        """Sets the access_expires of this UpdateAuthMethodGCP.

        Access expiration date in Unix timestamp (select 0 for access without expiry date)  # noqa: E501

        :param access_expires: The access_expires of this UpdateAuthMethodGCP.  # noqa: E501
        :type: int
        """

        self._access_expires = access_expires

    @property
    def audience(self):
        """Gets the audience of this UpdateAuthMethodGCP.  # noqa: E501

        The audience to verify in the JWT received by the client  # noqa: E501

        :return: The audience of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._audience

    @audience.setter
    def audience(self, audience):
        """Sets the audience of this UpdateAuthMethodGCP.

        The audience to verify in the JWT received by the client  # noqa: E501

        :param audience: The audience of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and audience is None:  # noqa: E501
            raise ValueError("Invalid value for `audience`, must not be `None`")  # noqa: E501

        self._audience = audience

    @property
    def bound_ips(self):
        """Gets the bound_ips of this UpdateAuthMethodGCP.  # noqa: E501

        A CIDR whitelist with the IPs that the access is restricted to  # noqa: E501

        :return: The bound_ips of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: list[str]
        """
        return self._bound_ips

    @bound_ips.setter
    def bound_ips(self, bound_ips):
        """Sets the bound_ips of this UpdateAuthMethodGCP.

        A CIDR whitelist with the IPs that the access is restricted to  # noqa: E501

        :param bound_ips: The bound_ips of this UpdateAuthMethodGCP.  # noqa: E501
        :type: list[str]
        """

        self._bound_ips = bound_ips

    @property
    def bound_labels(self):
        """Gets the bound_labels of this UpdateAuthMethodGCP.  # noqa: E501

        A comma-separated list of GCP labels formatted as \"key:value\" strings that must be set on authorized GCE instances. TODO: Because GCP labels are not currently ACL'd ....  # noqa: E501

        :return: The bound_labels of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: list[str]
        """
        return self._bound_labels

    @bound_labels.setter
    def bound_labels(self, bound_labels):
        """Sets the bound_labels of this UpdateAuthMethodGCP.

        A comma-separated list of GCP labels formatted as \"key:value\" strings that must be set on authorized GCE instances. TODO: Because GCP labels are not currently ACL'd ....  # noqa: E501

        :param bound_labels: The bound_labels of this UpdateAuthMethodGCP.  # noqa: E501
        :type: list[str]
        """

        self._bound_labels = bound_labels

    @property
    def bound_projects(self):
        """Gets the bound_projects of this UpdateAuthMethodGCP.  # noqa: E501

        === Human and Machine authentication section === Array of GCP project IDs. Only entities belonging to any of the provided projects can authenticate.  # noqa: E501

        :return: The bound_projects of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: list[str]
        """
        return self._bound_projects

    @bound_projects.setter
    def bound_projects(self, bound_projects):
        """Sets the bound_projects of this UpdateAuthMethodGCP.

        === Human and Machine authentication section === Array of GCP project IDs. Only entities belonging to any of the provided projects can authenticate.  # noqa: E501

        :param bound_projects: The bound_projects of this UpdateAuthMethodGCP.  # noqa: E501
        :type: list[str]
        """

        self._bound_projects = bound_projects

    @property
    def bound_regions(self):
        """Gets the bound_regions of this UpdateAuthMethodGCP.  # noqa: E501

        List of regions that a GCE instance must belong to in order to be authenticated. TODO: If bound_instance_groups is provided, it is assumed to be a regional group and the group must belong to this region. If bound_zones are provided, this attribute is ignored.  # noqa: E501

        :return: The bound_regions of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: list[str]
        """
        return self._bound_regions

    @bound_regions.setter
    def bound_regions(self, bound_regions):
        """Sets the bound_regions of this UpdateAuthMethodGCP.

        List of regions that a GCE instance must belong to in order to be authenticated. TODO: If bound_instance_groups is provided, it is assumed to be a regional group and the group must belong to this region. If bound_zones are provided, this attribute is ignored.  # noqa: E501

        :param bound_regions: The bound_regions of this UpdateAuthMethodGCP.  # noqa: E501
        :type: list[str]
        """

        self._bound_regions = bound_regions

    @property
    def bound_service_accounts(self):
        """Gets the bound_service_accounts of this UpdateAuthMethodGCP.  # noqa: E501

        List of service accounts the service account must be part of in order to be authenticated.  # noqa: E501

        :return: The bound_service_accounts of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: list[str]
        """
        return self._bound_service_accounts

    @bound_service_accounts.setter
    def bound_service_accounts(self, bound_service_accounts):
        """Sets the bound_service_accounts of this UpdateAuthMethodGCP.

        List of service accounts the service account must be part of in order to be authenticated.  # noqa: E501

        :param bound_service_accounts: The bound_service_accounts of this UpdateAuthMethodGCP.  # noqa: E501
        :type: list[str]
        """

        self._bound_service_accounts = bound_service_accounts

    @property
    def bound_zones(self):
        """Gets the bound_zones of this UpdateAuthMethodGCP.  # noqa: E501

        === Machine authentication section === List of zones that a GCE instance must belong to in order to be authenticated. TODO: If bound_instance_groups is provided, it is assumed to be a zonal group and the group must belong to this zone.  # noqa: E501

        :return: The bound_zones of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: list[str]
        """
        return self._bound_zones

    @bound_zones.setter
    def bound_zones(self, bound_zones):
        """Sets the bound_zones of this UpdateAuthMethodGCP.

        === Machine authentication section === List of zones that a GCE instance must belong to in order to be authenticated. TODO: If bound_instance_groups is provided, it is assumed to be a zonal group and the group must belong to this zone.  # noqa: E501

        :param bound_zones: The bound_zones of this UpdateAuthMethodGCP.  # noqa: E501
        :type: list[str]
        """

        self._bound_zones = bound_zones

    @property
    def force_sub_claims(self):
        """Gets the force_sub_claims of this UpdateAuthMethodGCP.  # noqa: E501

        if true: enforce role-association must include sub claims  # noqa: E501

        :return: The force_sub_claims of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: bool
        """
        return self._force_sub_claims

    @force_sub_claims.setter
    def force_sub_claims(self, force_sub_claims):
        """Sets the force_sub_claims of this UpdateAuthMethodGCP.

        if true: enforce role-association must include sub claims  # noqa: E501

        :param force_sub_claims: The force_sub_claims of this UpdateAuthMethodGCP.  # noqa: E501
        :type: bool
        """

        self._force_sub_claims = force_sub_claims

    @property
    def name(self):
        """Gets the name of this UpdateAuthMethodGCP.  # noqa: E501

        Auth Method name  # noqa: E501

        :return: The name of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateAuthMethodGCP.

        Auth Method name  # noqa: E501

        :param name: The name of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this UpdateAuthMethodGCP.  # noqa: E501

        Auth Method new name  # noqa: E501

        :return: The new_name of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this UpdateAuthMethodGCP.

        Auth Method new name  # noqa: E501

        :param new_name: The new_name of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def password(self):
        """Gets the password of this UpdateAuthMethodGCP.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The password of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this UpdateAuthMethodGCP.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param password: The password of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def service_account_creds_data(self):
        """Gets the service_account_creds_data of this UpdateAuthMethodGCP.  # noqa: E501

        ServiceAccount credentials data instead of giving a file path, base64 encoded  # noqa: E501

        :return: The service_account_creds_data of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._service_account_creds_data

    @service_account_creds_data.setter
    def service_account_creds_data(self, service_account_creds_data):
        """Sets the service_account_creds_data of this UpdateAuthMethodGCP.

        ServiceAccount credentials data instead of giving a file path, base64 encoded  # noqa: E501

        :param service_account_creds_data: The service_account_creds_data of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """

        self._service_account_creds_data = service_account_creds_data

    @property
    def token(self):
        """Gets the token of this UpdateAuthMethodGCP.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UpdateAuthMethodGCP.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def type(self):
        """Gets the type of this UpdateAuthMethodGCP.  # noqa: E501

        Type of the GCP Access Rules  # noqa: E501

        :return: The type of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UpdateAuthMethodGCP.

        Type of the GCP Access Rules  # noqa: E501

        :param type: The type of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def uid_token(self):
        """Gets the uid_token of this UpdateAuthMethodGCP.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this UpdateAuthMethodGCP.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this UpdateAuthMethodGCP.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def username(self):
        """Gets the username of this UpdateAuthMethodGCP.  # noqa: E501

        Required only when the authentication process requires a username and password  # noqa: E501

        :return: The username of this UpdateAuthMethodGCP.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this UpdateAuthMethodGCP.

        Required only when the authentication process requires a username and password  # noqa: E501

        :param username: The username of this UpdateAuthMethodGCP.  # noqa: E501
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
        if not isinstance(other, UpdateAuthMethodGCP):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateAuthMethodGCP):
            return True

        return self.to_dict() != other.to_dict()
