# coding: utf-8

"""
    BIMData API

    BIMData API is a tool to interact with your models stored on BIMData’s servers.     Through the API, you can manage your projects, the clouds, upload your IFC files and manage them through endpoints.  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: support@bimdata.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import bimdata_api_client
from bimdata_api_client.models.self_user import SelfUser  # noqa: E501
from bimdata_api_client.rest import ApiException

class TestSelfUser(unittest.TestCase):
    """SelfUser unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SelfUser
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = bimdata_api_client.models.self_user.SelfUser()  # noqa: E501
        if include_optional :
            return SelfUser(
                id = 56, 
                email = '0', 
                firstname = '0', 
                lastname = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                organizations = [
                    bimdata_api_client.models.organization.Organization(
                        id = 56, 
                        name = '0', 
                        is_personnal = True, 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        logo = '0', )
                    ], 
                clouds = [
                    bimdata_api_client.models.cloud_role.CloudRole(
                        cloud = 56, 
                        role = 56, )
                    ], 
                projects = [
                    bimdata_api_client.models.project_role.ProjectRole(
                        project = 56, 
                        role = 56, )
                    ], 
                provider = '0', 
                provider_sub = '0', 
                sub = '0', 
                profile_picture = '0'
            )
        else :
            return SelfUser(
                email = '0',
                firstname = '0',
                lastname = '0',
        )

    def testSelfUser(self):
        """Test SelfUser"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
