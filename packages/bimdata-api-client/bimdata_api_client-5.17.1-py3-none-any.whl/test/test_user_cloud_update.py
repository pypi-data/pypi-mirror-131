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
from bimdata_api_client.models.user_cloud_update import UserCloudUpdate  # noqa: E501
from bimdata_api_client.rest import ApiException

class TestUserCloudUpdate(unittest.TestCase):
    """UserCloudUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test UserCloudUpdate
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = bimdata_api_client.models.user_cloud_update.UserCloudUpdate()  # noqa: E501
        if include_optional :
            return UserCloudUpdate(
                role = 56
            )
        else :
            return UserCloudUpdate(
        )

    def testUserCloudUpdate(self):
        """Test UserCloudUpdate"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
