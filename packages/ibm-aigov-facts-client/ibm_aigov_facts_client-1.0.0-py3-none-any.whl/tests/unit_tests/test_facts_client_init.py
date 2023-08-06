# coding: utf-8

# Copyright 2020-2021 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import unittest
from ibm_aigov_facts_client import AIGovFactsClient
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from tests.utils.config import get_facts_client_credentials

from ibm_aigov_facts_client.utils.client_errors import AuthorizationError


def remove_folder(path):
    # check if folder exists
    if os.path.exists(path):
        # remove if exists
        shutil.rmtree(path)


remove_folder("mlruns")
remove_folder("logs")


class TestClientInitialization(unittest.TestCase):
    api_key = None
    iam_credentials = None
    exp_name = None
    container_type = None
    container_id = None

    @classmethod
    def setUpClass(cls):
        cls.iam_credentials = get_facts_client_credentials()
        cls.apikey = cls.iam_credentials['apikey']
        cls.exp_name = cls.iam_credentials['exp_name']
        cls.container_type = cls.iam_credentials['container_type']
        cls.container_id = cls.iam_credentials['container_id']

    def test_01_initialize_client__init(self):
        ai_client_v2 = AIGovFactsClient(
            api_key=TestClientInitialization.apikey, experiment_name=TestClientInitialization.exp_name, container_type=TestClientInitialization.container_type, container_id=TestClientInitialization.container_id
        )
        print(ai_client_v2.version)
        print(ai_client_v2.experiment_name)


if __name__ == '__main__':
    unittest.main()
