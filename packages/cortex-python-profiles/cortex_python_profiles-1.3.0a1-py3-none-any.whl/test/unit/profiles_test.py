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
import logging
import unittest

from cortex import Cortex
from mocket import mocketize
from mocket.mockhttp import Entry

from cortex_profiles import ProfileClient
from cortex_profiles.ext.rest import ProfilesRestClient
from .fixtures import john_doe_token, build_mock_url, mock_api_endpoint, register_entry_from_path

log = logging.getLogger()


@unittest.skip("skipping test for dependency issue")
class TestProfile(unittest.TestCase):

    def setUp(self):
        # Initialize Clients ...
        client = Cortex.client(api_endpoint=mock_api_endpoint(), token=john_doe_token(), project="sreddy4")
        self.project_id = "sreddy4"
        self.cortex = ProfileClient(client)
        self.profiles_client = ProfilesRestClient(client)

        self.profile_id = "07C68D9A1FC5"
        self.schema_name = "member-stream2-8d02a"
        self.schema_id = self.schema_name

    @mocketize
    def test_list_schemas_with_client(self):
        """
        Tests getting schemas from a mocked endpoint ...
        :return:
        """
        register_entry_from_path(
            Entry.POST,
            build_mock_url(ProfilesRestClient.URIs["profiles"]), './test/data/schemas/list_schemas.json')
        schemas = self.profiles_client.list_schemas()
        self.assertEqual(len(schemas), 1)
        self.assertEqual(schemas[0].name, self.schema_name)

    @mocketize
    def test_get_schema_with_builder_pattern(self):
        register_entry_from_path(
            Entry.POST,
            build_mock_url(ProfilesRestClient.URIs["profiles"]), './test/data/schemas/schema.json')
        schema = self.cortex.profile_schema(self.schema_id).latest()
        self.assertIsNotNone(schema)
        self.assertEqual(schema.name, self.schema_name)

    @mocketize
    def test_list_profiles_with_client(self):
        """
        Tests getting schemas from a mocked endpoint ...
        :return:
        """
        register_entry_from_path(
            Entry.POST,
            build_mock_url(ProfilesRestClient.URIs["profiles"]), './test/data/list_profiles.json')
        profiles = self.profiles_client.find_profiles(profile_schema=self.schema_id, attributes=["email", "state"])
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0].profileID, self.profile_id)

    @mocketize
    def test_get_latest_profile_with_client(self):
        """
        Tests getting schemas from a mocked endpoint ...
        :return:
        """
        register_entry_from_path(
            Entry.POST,
            build_mock_url(ProfilesRestClient.URIs["profiles"]),
            "./test/data/get_latest_profile.json"
        )
        profile = self.profiles_client.describe_profile(self.profile_id, self.schema_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.profileID, self.profile_id)

    @mocketize
    def test_get_latest_profile_with_builder_pattern(self):
        register_entry_from_path(
            Entry.POST,
            build_mock_url(ProfilesRestClient.URIs["profiles"]),
            "./test/data/get_latest_profile.json"
        )
        profile = self.cortex.profile(self.profile_id, self.schema_id).latest()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.profileID, self.profile_id)
