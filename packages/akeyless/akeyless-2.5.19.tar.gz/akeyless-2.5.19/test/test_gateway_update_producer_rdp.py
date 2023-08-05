# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import akeyless
from akeyless.models.gateway_update_producer_rdp import GatewayUpdateProducerRdp  # noqa: E501
from akeyless.rest import ApiException

class TestGatewayUpdateProducerRdp(unittest.TestCase):
    """GatewayUpdateProducerRdp unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GatewayUpdateProducerRdp
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.gateway_update_producer_rdp.GatewayUpdateProducerRdp()  # noqa: E501
        if include_optional :
            return GatewayUpdateProducerRdp(
                fixed_user_only = 'false', 
                name = '0', 
                new_name = '0', 
                password = '0', 
                producer_encryption_key_name = '0', 
                rdp_admin_name = '0', 
                rdp_admin_pwd = '0', 
                rdp_host_name = '0', 
                rdp_host_port = '22', 
                rdp_user_groups = '0', 
                secure_access_allow_external_user = True, 
                secure_access_enable = '0', 
                secure_access_host = [
                    '0'
                    ], 
                secure_access_rdp_domain = '0', 
                secure_access_rdp_user = '0', 
                target_name = '0', 
                token = '0', 
                uid_token = '0', 
                user_ttl = '60m', 
                username = '0'
            )
        else :
            return GatewayUpdateProducerRdp(
                name = '0',
        )

    def testGatewayUpdateProducerRdp(self):
        """Test GatewayUpdateProducerRdp"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
