# coding: utf-8

# Copyright 2020,2021 IBM All Rights Reserved.
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


import logging
import jwt
import json
import requests
import pandas as pd

from ibm_cloud_sdk_core.authenticators.iam_authenticator import IAMAuthenticator
from ibm_aigov_facts_client.utils.client_errors import *
from ibm_aigov_facts_client.utils.enums import FactsheetAssetType
from ibm_aigov_facts_client.utils.utils import validate_enum

from ..utils.config import *


_logger = logging.getLogger(__name__)


class FactSheetElements:

    def __init__(self):
        self.api_key = None
        self.type_name = None

    def _get_token(self, api_key):

        if api_key:
            try:
                if get_env() is None or get_env() == 'prod':
                    _authenticator = IAMAuthenticator(
                        apikey=api_key)

                elif get_env() == 'dev' or get_env() == 'test':
                    _authenticator = IAMAuthenticator(
                        apikey=api_key, url=dev_config['IAM_URL'])
                else:
                    _authenticator = IAMAuthenticator(
                        apikey=api_key)
            except:
                raise AuthorizationError(
                    "Something went wrong when initiating Authentication")

        if isinstance(_authenticator, IAMAuthenticator):
            token = _authenticator.token_manager.get_token()
        else:
            token = _authenticator.bearer_token
        return token

    def _get_bss_id(self, api_key):
        try:
            token = self._get_token(api_key)
            decoded_bss_id = jwt.decode(token, options={"verify_signature": False})[
                "account"]["bss"]
        except jwt.ExpiredSignatureError:
            raise
        return decoded_bss_id

    def _get_current_assets_prop(self, asset_type=FactsheetAssetType.MODEL_FACTS_USER):
        headers = {}
        cur_bss_id = self._get_bss_id(self.api_key)
        _logger.debug("current bss_id {}".format(cur_bss_id))
        headers["Authorization"] = "Bearer " + self._get_token(self.api_key)
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        params = {"bss_account_id": cur_bss_id}

        if get_env() == 'dev':
            url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                '/v2/asset_types/' + asset_type
        elif get_env() == 'test':
            url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                '/v2/asset_types/'+asset_type
        else:
            url = prod_config["DEFAULT_SERVICE_URL"] + \
                '/v2/asset_types'+asset_type

        _logger.debug("current url {}".format(url))
        response = requests.get(url=url,
                                headers=headers,
                                params=params)

        if not response:
            ClientError("Current asset properties not found")
            raise

        if response.status_code == 403:
            _logger.exception(response.json()['message'])
            raise

        elif response.status_code == 401:
            _logger.exception("Expired token found.")
            raise

        elif response.status_code == 200:
            current_asset_prop = response.json()
            _logger.debug("Response...{}".format(response.json()))
        return current_asset_prop

    def _file_data_validation(self, name, props):

        if not name or not props['type'] or not props['label']:
            raise MissingValue("Property name or type or label")

        if props["type"].lower() != "string" and props["type"].lower() != "integer" and props["type"].lower() != "date":
            raise UnexpectedValue(
                "Only string, integer and date type is supported ")

        if (props["type"].lower() == "string") and (props["minimum"] != '' or props["maximum"] != ''):
            raise UnexpectedValue(
                "For String type, ONLY min and max length should be defined if applicable")

        if (props["type"].lower() == "integer") and (props["min_length"] != '' or props["max_length"] != ''):
            raise UnexpectedValue(
                "For Integer type, ONLY minimum and maximum value should be defined if applicable")

    def _get_props_from_file(self, data):
        props = {}
        fields = []
        global_search = []

        for _, row in data.iterrows():
            tmp_props = {}

            name = row["name"]
            tmp_props["type"] = row["type"]
            tmp_props["description"] = row["description"]
            tmp_props["placeholder"] = row["placeholder"]

            tmp_props["is_array"] = row["is_array"] or False
            tmp_props["required"] = row["required"] or True
            tmp_props["hidden"] = row["hidden"] or False
            tmp_props["readonly"] = row["readonly"] or False

            tmp_props["default_value"] = row["default_value"]
            tmp_props["minimum"] = row["minimum"]
            tmp_props["maximum"] = row["maximum"]
            tmp_props["min_length"] = row["min_length"]
            tmp_props["max_length"] = row["max_length"]
            tmp_props["label"] = {"default": row["label"], "en": row["label"]}
            is_searchable = row["is_searchable"] or False

            props[row["name"]] = tmp_props
            self._file_data_validation(name, tmp_props)

            if is_searchable is True:
                fields_prop = {}
                fields_prop["key"] = row["name"]
                fields_prop["type"] = row["type"]
                fields_prop["facet"] = False
                fields_prop["is_array"] = row["is_array"]
                fields_prop["search_path"] = row["name"]
                fields_prop["is_searchable_across_types"] = False

                fields.append(fields_prop)

                global_search.append(name)
        return props, fields, global_search

    def _format_data(self, csvFilePath, overwrite, asset_type):
        props = {}
        fields = []
        global_search = []
        csv_data = pd.read_csv(csvFilePath, sep=",", na_filter=False)

        if csv_data.empty:
            raise ClientError("File can not be empty")

        props, fields, global_search = self._get_props_from_file(csv_data)

        if overwrite:
            final_dict = {}
            final_dict["description"] = "The model fact user asset type to capture user defined attributes."
            final_dict["fields"] = fields
            final_dict["relationships"] = []
            final_dict["global_search_searchable"] = global_search
            final_dict["properties"] = props

            if asset_type == FactsheetAssetType.MODEL_ENTRY_USER:
                final_dict["decorates"] = [{"asset_type_name": "model_entry"}]

            final_dict["localized_metadata_attributes"] = {
                "name": {"default": "Additional details", "en": "Additional details"}}

            _logger.debug("current json..{}".format(
                json.dumps(final_dict, indent=4)))
            return final_dict
        else:
            current_asset_props = self._get_current_assets_prop(asset_type)

            if current_asset_props and current_asset_props.get("properties"):

                if (current_asset_props["properties"] and props) or (not current_asset_props["properties"] and props):
                    current_asset_props["properties"].update(props)

                if (current_asset_props["fields"] and fields) or (not current_asset_props["fields"] and fields):
                    for field in fields:
                        current_asset_props["fields"].append(field)

                if (current_asset_props["global_search_searchable"] and global_search) or (not current_asset_props["global_search_searchable"] and global_search):
                    for global_search_item in global_search:
                        current_asset_props["global_search_searchable"].append(
                            global_search_item)
                entries_to_remove = ["name", "version", "scope"]
                list(map(current_asset_props.pop, entries_to_remove))
                _logger.debug(current_asset_props)

            elif current_asset_props and not current_asset_props.get("properties"):
                current_asset_props["properties"] = props
                if (current_asset_props["fields"] and fields) or (not current_asset_props["fields"] and fields):
                    for field in fields:
                        current_asset_props["fields"].append(field)

                if (current_asset_props["global_search_searchable"] and global_search) or (not current_asset_props["global_search_searchable"] and global_search):
                    for global_search_item in global_search:
                        current_asset_props["global_search_searchable"].append(
                            global_search_item)
                entries_to_remove = ["name", "version", "scope"]
                list(map(current_asset_props.pop, entries_to_remove))
                _logger.debug(current_asset_props)

            else:
                raise ClientError("Existing properties not found")

            return current_asset_props

    def replace_asset_properties(self, api_key, csvFilePath, type_name=None, overwrite=True):
        """
            Utility to add custom asset properties of model or model entry.

            :param str api_key: IBM Cloud API key
            :param str csvFilePath: File path of csv having the asset properties.
            :param str type_name: Asset type user needs to update. Current options are `modelfacts_user` and `model_entry_user`. Default is set to `modelfacts_user`
            :param bool overwrite: Merge or replace current properties. Default is to overwrite.

            A way you might use me is:

            >>> from ibm_aigov_facts_client import FactSheetElements
            >>> client = FactSheetElements()
            >>> client.replace_asset_properties("Asset_type_definition.csv")
            >>> client.factsheet_utils.replace_asset_properties("Asset_type_definition.csv",type_name="model_entry_user", overwrite=False)
        """
        self.api_key = api_key

        validate_enum(type_name,
                      "type_name", FactsheetAssetType, False)

        cur_bss_id = self._get_bss_id(self.api_key)

        self.type_name = type_name or FactsheetAssetType.MODEL_FACTS_USER

        asset_conf_data = self._format_data(
            csvFilePath, overwrite, self.type_name)

        _logger.debug("data;  {}".format(asset_conf_data))

        if asset_conf_data:
            self._update_props(asset_conf_data, cur_bss_id, self.type_name)
        else:
            raise ClientError("Error formatting properties data from file")

    def _update_props(self, data, bss_id, type_name):

        headers = {}
        headers["Authorization"] = "Bearer " + self._get_token(self.api_key)
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        params = {"bss_account_id": bss_id}

        if get_env() == 'dev':
            url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                '/v2/asset_types/'+type_name
        elif get_env() == 'test':
            url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                '/v2/asset_types/'+type_name
        else:
            url = prod_config["DEFAULT_SERVICE_URL"] + \
                '/v2/asset_types/'+type_name

        _logger.debug("url...{}".format(url))
        response = requests.put(url=url,
                                headers=headers,
                                params=params,
                                data=json.dumps(data))

        if response.status_code == 401:
            _logger.exception("Expired token found.")
            raise
        elif response.status_code == 200:
            _logger.info("Asset properties updated Successfully")
        else:
            _logger.exception(
                "Error updating properties..{}".format(response.json()))
