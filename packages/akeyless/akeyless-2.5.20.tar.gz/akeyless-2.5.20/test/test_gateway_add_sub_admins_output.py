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
from akeyless.models.gateway_add_sub_admins_output import GatewayAddSubAdminsOutput  # noqa: E501
from akeyless.rest import ApiException

class TestGatewayAddSubAdminsOutput(unittest.TestCase):
    """GatewayAddSubAdminsOutput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GatewayAddSubAdminsOutput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.gateway_add_sub_admins_output.GatewayAddSubAdminsOutput()  # noqa: E501
        if include_optional :
            return GatewayAddSubAdminsOutput(
                sub_admins = [
                    '0'
                    ]
            )
        else :
            return GatewayAddSubAdminsOutput(
        )

    def testGatewayAddSubAdminsOutput(self):
        """Test GatewayAddSubAdminsOutput"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
