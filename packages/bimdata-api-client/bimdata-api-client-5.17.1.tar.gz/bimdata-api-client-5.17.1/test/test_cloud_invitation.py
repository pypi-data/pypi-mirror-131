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
from bimdata_api_client.models.cloud_invitation import CloudInvitation  # noqa: E501
from bimdata_api_client.rest import ApiException

class TestCloudInvitation(unittest.TestCase):
    """CloudInvitation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CloudInvitation
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = bimdata_api_client.models.cloud_invitation.CloudInvitation()  # noqa: E501
        if include_optional :
            return CloudInvitation(
                id = 56, 
                email = '0', 
                redirect_uri = '0', 
                role = 56
            )
        else :
            return CloudInvitation(
                email = '0',
                redirect_uri = '0',
        )

    def testCloudInvitation(self):
        """Test CloudInvitation"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
