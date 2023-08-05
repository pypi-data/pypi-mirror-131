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
from bimdata_api_client.models.check_plan import CheckPlan  # noqa: E501
from bimdata_api_client.rest import ApiException

class TestCheckPlan(unittest.TestCase):
    """CheckPlan unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CheckPlan
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = bimdata_api_client.models.check_plan.CheckPlan()  # noqa: E501
        if include_optional :
            return CheckPlan(
                id = 56, 
                name = '0', 
                description = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                rulesets = [
                    bimdata_api_client.models.ruleset.Ruleset(
                        id = 56, 
                        parent_ruleset_id = 56, 
                        name = '0', 
                        description = '0', 
                        rules = [
                            bimdata_api_client.models.rule.Rule(
                                id = 56, 
                                name = '0', 
                                condition = '0', 
                                rule_components = [
                                    bimdata_api_client.models.rule_component.RuleComponent(
                                        id = 56, 
                                        type = '0', 
                                        value = bimdata_api_client.models.value.Value(), 
                                        operator = '0', 
                                        params = bimdata_api_client.models.params.Params(), 
                                        condition = '0', )
                                    ], 
                                on = bimdata_api_client.models.rule.Rule(
                                    id = 56, 
                                    name = '0', 
                                    condition = '0', ), )
                            ], 
                        rulesets = [
                            bimdata_api_client.models.ruleset.Ruleset(
                                id = 56, 
                                parent_ruleset_id = 56, 
                                name = '0', 
                                description = '0', )
                            ], )
                    ], 
                is_default = True
            )
        else :
            return CheckPlan(
                name = '0',
        )

    def testCheckPlan(self):
        """Test CheckPlan"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
