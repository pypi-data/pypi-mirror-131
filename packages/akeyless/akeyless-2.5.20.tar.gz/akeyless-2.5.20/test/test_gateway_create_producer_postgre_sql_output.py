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
from akeyless.models.gateway_create_producer_postgre_sql_output import GatewayCreateProducerPostgreSQLOutput  # noqa: E501
from akeyless.rest import ApiException

class TestGatewayCreateProducerPostgreSQLOutput(unittest.TestCase):
    """GatewayCreateProducerPostgreSQLOutput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GatewayCreateProducerPostgreSQLOutput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.gateway_create_producer_postgre_sql_output.GatewayCreateProducerPostgreSQLOutput()  # noqa: E501
        if include_optional :
            return GatewayCreateProducerPostgreSQLOutput(
                producer_details = akeyless.models.ds_producer_details.DSProducerDetails(
                    active = True, 
                    admin_name = '0', 
                    admin_pwd = '0', 
                    admin_rotation_interval_days = 56, 
                    allow_subdomains = True, 
                    allowed_domains = '0', 
                    artifactory_admin_apikey = '0', 
                    artifactory_admin_username = '0', 
                    artifactory_base_url = '0', 
                    artifactory_token_audience = '0', 
                    artifactory_token_scope = '0', 
                    auto_generated_folder = '0', 
                    aws_access_key_id = '0', 
                    aws_access_mode = '0', 
                    aws_region = '0', 
                    aws_role_arns = '0', 
                    aws_secret_access_key = '0', 
                    aws_session_token = '0', 
                    aws_user_console_access = True, 
                    aws_user_groups = '0', 
                    aws_user_policies = '0', 
                    aws_user_programmatic_access = True, 
                    azure_app_object_id = '0', 
                    azure_client_id = '0', 
                    azure_client_secret = '0', 
                    azure_tenant_id = '0', 
                    azure_user_groups_obj_id = '0', 
                    azure_user_portal_access = True, 
                    azure_user_programmatic_access = True, 
                    azure_user_roles_template_id = '0', 
                    chef_organizations = '0', 
                    chef_server_access_mode = '0', 
                    chef_server_host_name = '0', 
                    chef_server_key = '0', 
                    chef_server_port = '0', 
                    chef_server_url = '0', 
                    chef_server_username = '0', 
                    chef_skip_ssl = True, 
                    create_cert_using_pki = True, 
                    db_host_name = '0', 
                    db_isolation_level = '0', 
                    db_max_idle_conns = '0', 
                    db_max_open_conns = '0', 
                    db_name = '0', 
                    db_port = '0', 
                    db_pwd = '0', 
                    db_server_certificates = '0', 
                    db_server_name = '0', 
                    db_user_name = '0', 
                    dynamic_secret_id = 56, 
                    dynamic_secret_key = '0', 
                    dynamic_secret_name = '0', 
                    dynamic_secret_type = '0', 
                    eks_access_key_id = '0', 
                    eks_assume_role = '0', 
                    eks_cluster_ca_certificate = '0', 
                    eks_cluster_endpoint = '0', 
                    eks_cluster_name = '0', 
                    eks_region = '0', 
                    eks_secret_access_key = '0', 
                    enable_admin_rotation = True, 
                    failure_message = '0', 
                    fixed_user_only = '0', 
                    gke_cluster_ca_certificate = '0', 
                    gke_cluster_compute_zone = '0', 
                    gke_cluster_endpoint = '0', 
                    gke_cluster_name = '0', 
                    gke_project_id = '0', 
                    gke_service_account_key = '0', 
                    gke_service_account_name = '0', 
                    groups = '0', 
                    host_name = '0', 
                    host_port = '0', 
                    mongodb_db_name = '0', 
                    mongodb_roles = '0', 
                    mongodb_uri_connection = '0', 
                    mssql_creation_statements = '0', 
                    mssql_revocation_statements = '0', 
                    mysql_creation_statements = '0', 
                    postgres_creation_statements = '0', 
                    rabbitmq_server_password = '0', 
                    rabbitmq_server_uri = '0', 
                    rabbitmq_server_user = '0', 
                    rabbitmq_user_conf_permission = '0', 
                    rabbitmq_user_read_permission = '0', 
                    rabbitmq_user_tags = '0', 
                    rabbitmq_user_vhost = '0', 
                    rabbitmq_user_write_permission = '0', 
                    root_first_in_chain = True, 
                    should_stop = '0', 
                    signer_key_name = '0', 
                    store_private_key = True, 
                    user_principal_name = '0', 
                    user_ttl = '0', 
                    venafi_api_key = '0', 
                    venafi_zone = '0', )
            )
        else :
            return GatewayCreateProducerPostgreSQLOutput(
        )

    def testGatewayCreateProducerPostgreSQLOutput(self):
        """Test GatewayCreateProducerPostgreSQLOutput"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
