"""
Copyright 2021 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
import logging
import unittest
import attr

from cortex_profiles.ext.builders import ProfileSchemaBuilder
from cortex_common.types.schemas import ProfileSchema, DataSourceSelection, TimestampSpec, ProfileNames

log = logging.getLogger()


@unittest.skip("skipping test for dependency issue")
class TestProfileBuilder(unittest.TestCase):

    def setUp(self):
        self.schema = ProfileSchemaBuilder.append_from_schema_json("./test/data/schemas/schema.json")

    def test_01_building_schemas_from_json(self):
        """
        Tests build schemas from a json file ...
        :return:
        """
        schema = ProfileSchemaBuilder.append_from_schema_json("./test/data/schemas/schema.json")
        log.debug(json.dumps(attr.asdict(schema), indent=4))
        self.assertTrue(isinstance(schema, ProfileSchema))
        self.assertFalse(schema is None)

    def test_02_building_schema(self):
        """
        Tests build schema by appending attributes
        :return:
        """
        project = "test1"
        builder = ProfileSchemaBuilder("test-schema-1234")
        primary_source = DataSourceSelection(name="streamdata-par-14df0",
                                             attributes=["Email", "ZipCode", "State", "Date", "Gender", "Age", "Phone"],
                                             profileKey="AccountId", timestamp=TimestampSpec(auto=True))
        names = ProfileNames(singular="member", plural="members", title="Member Schema 1234", categories=["member"])
        schema = builder.title("Test Schema 1234").description("Description").names(names).project(
            project).primary_source(primary_source).build()
        log.debug(json.dumps(attr.asdict(schema), indent=4))
        self.assertTrue(isinstance(schema, ProfileSchema))
        self.assertFalse(schema is None)

    def test_03_profile_schema_equality(self):
        self.assertEqual(
            ProfileSchemaBuilder("test-schema-1234").title("Test Schema 1234").description("Description").names(
                ProfileNames(singular="member", plural="members", title="Member Schema 1234",
                             categories=["member"])).project("test1").primary_source(
                DataSourceSelection(name="streamdata-par-14df0",
                                    attributes=["Email", "ZipCode", "State", "Date", "Gender", "Age", "Phone"],
                                    profileKey="AccountId", timestamp=TimestampSpec(auto=True))).build(),
            ProfileSchemaBuilder("test-schema-1234").title("Test Schema 1234").description(
                "Description").names(
                ProfileNames(singular="member", plural="members", title="Member Schema 1234",
                             categories=["member"])).project("test1").primary_source(
                DataSourceSelection(name="streamdata-par-14df0",
                                    attributes=["Email", "ZipCode", "State", "Date", "Gender", "Age", "Phone"],
                                    profileKey="AccountId", timestamp=TimestampSpec(auto=True))).build()
        )
