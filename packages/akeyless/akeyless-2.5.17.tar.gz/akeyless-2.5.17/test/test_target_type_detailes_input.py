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
from akeyless.models.target_type_detailes_input import TargetTypeDetailesInput  # noqa: E501
from akeyless.rest import ApiException

class TestTargetTypeDetailesInput(unittest.TestCase):
    """TargetTypeDetailesInput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TargetTypeDetailesInput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.target_type_detailes_input.TargetTypeDetailesInput()  # noqa: E501
        if include_optional :
            return TargetTypeDetailesInput(
                admin_name = '0', 
                admin_pwd = '0', 
                aws_access_key_id = '0', 
                aws_region = '0', 
                aws_secret_access_key = '0', 
                aws_session_token = '0', 
                db_host_name = '0', 
                db_port = '0', 
                db_pwd = '0', 
                db_user_name = '0', 
                host_name = '0', 
                host_port = '0', 
                ip = [
                    '0'
                    ], 
                mongodb_db_name = '0', 
                mongodb_uri_connection = '0', 
                port = '0', 
                rabbitmq_server_password = '0', 
                rabbitmq_server_uri = '0', 
                rabbitmq_server_user = '0', 
                url = '0'
            )
        else :
            return TargetTypeDetailesInput(
        )

    def testTargetTypeDetailesInput(self):
        """Test TargetTypeDetailesInput"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
