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
from typing import Dict
import jwt
import json
import requests
import pandas as pd
import hashlib

from ibm_cloud_sdk_core.authenticators.iam_authenticator import IAMAuthenticator
from ibm_aigov_facts_client.client import fact_trace, autolog, manual_log
from ibm_aigov_facts_client.utils.client_errors import *
from ibm_aigov_facts_client.utils.enums import FactsheetAssetType
from ibm_aigov_facts_client.utils.utils import validate_enum
from ibm_cloud_sdk_core.utils import convert_list, convert_model

from typing import BinaryIO, Dict, List, TextIO, Union

from ..utils.config import *


_logger = logging.getLogger(__name__)


class ExternalModelFactsElements:

    def __init__(self,api_key:str, experiment_name:str):

        self.api_key = api_key
        self.experiment_name = experiment_name
    
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

    def _encode_model_id(self,model_id):
        encoded_id=hashlib.md5(model_id.encode("utf-8")).hexdigest()
        return encoded_id

    def _encode_deployment_id(self,deployment_id):
        encoded_deployment_id=hashlib.md5(deployment_id.encode("utf-8")).hexdigest()
        return encoded_deployment_id

    def _validate_payload(self, payload):
        if not payload["model_id"] or not payload["name"]:
            raise ClientError("model_identifier or name is missing")
        else:
            payload["model_id"]= self._encode_model_id(payload["model_id"])
        if payload["deployment_details"]:
            _logger.debug("details {}".format(payload))
            payload["deployment_details"]["id"]= self._encode_deployment_id(payload["deployment_details"]["id"])

        return payload


    def save_external_model_asset(self, model_identifier:str, name:str, description:str=None, schemas:'ExternalModelSchemas'=None, training_data_reference:'TrainingDataReference'=None,deployment_details:'DeploymentDetails'=None):
        
        """
        Save External model assets in catalog.

        :param str model_identifier: Identifier specific to ML providers (i.e., Azure ML service: `service_id`, AWS Sagemaker:`model_name`)
        :param str name: Name of the model
        :param str description: (Optional) description of the model
        :param ExternalModelSchemas schemas: (Optional) Input and Output schema of the model
        :param TrainingDataReference training_data_reference: (Optional) Training data schema
        :param DeploymentDetails deployment_details: (Optional) Model deployment details


        If using external models with manual log option, initiate client as:

        .. code-block:: python

            from ibm_aigov_facts_client import AIGovFactsClient,DeploymentDetails,TrainingDataReference,ExternalModelSchemas
            client= AIGovFactsClient(api_key=API_KEY,experiment_name="external",enable_autolog=False,external_model=True)


        If using external models with Autolog, initiate client as:

        .. code-block:: python

            from ibm_aigov_facts_client import AIGovFactsClient,DeploymentDetails,TrainingDataReference,ExternalModelSchemas
            client= AIGovFactsClient(api_key=API_KEY,experiment_name="external",external_model=True)

            
        Payload example by supported external providers:

        Azure ML Service:

        .. code-block:: python

            external_schemas=ExternalModelSchemas(input=input_schema,output=output_schema)
            trainingdataref=TrainingDataReference(schema=training_ref)
            deployment=DeploymentDetails(identifier=<service_url in Azure>,name="deploymentname",deployment_type="online",scoring_endpoint="test/score")

            facts_client.external_model_facts.save_external_model_asset(model_identifier=<service_id in Azure>
                                                                        ,name=<model_name>
                                                                        ,deployment_details=deployment
                                                                        ,schemas=external_schemas
                                                                        ,training_data_reference=tdataref)


        AWS Sagemaker:

        .. code-block:: python

            external_schemas=ExternalModelSchemas(input=input_schema,output=output_schema)
            trainingdataref=TrainingDataReference(schema=training_ref)
            deployment=DeploymentDetails(identifier=<endpoint_name in Sagemaker>,name="deploymentname",deployment_type="online",scoring_endpoint="test/score")

            facts_client.external_model_facts.save_external_model_asset(model_identifier=<model_name in Sagemaker>
                                                                        ,name=<model_name>
                                                                        ,deployment_details=deployment
                                                                        ,schemas=external_schemas
                                                                        ,training_data_reference=tdataref)
        """
        
        if deployment_details:
            deployment_details=convert_model(deployment_details)
        if schemas:
            schemas=convert_model(schemas)
        if training_data_reference:
            training_data_reference=convert_model(training_data_reference)
        
        
        data = {
            'model_id': model_identifier,
            'name': name,
            'description': description,
            'schemas': schemas,
            'training_data_references': training_data_reference,
            'deployment_details': deployment_details
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        _validated_payload= self._validate_payload(data) 
        _logger.debug("validated payload..{}".format(_validated_payload))
        self._publish(_validated_payload)  



    def _publish(self, data):

        headers = {}
        headers["Authorization"] = "Bearer " + self._get_token(self.api_key)
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        params = {"experiment_name": self.experiment_name}

        if get_env() == 'dev':
            url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                '/v1/aigov/model_inventory/model_stub'
        elif get_env() == 'test':
            url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                '/v1/aigov/model_inventory/model_stub'
        else:
            url = prod_config["DEFAULT_SERVICE_URL"] + \
                '/v1/aigov/model_inventory/model_stub'

        _logger.debug("url...{}".format(url))
        response = requests.put(url=url,
                                headers=headers,
                                params=params,
                                data=json.dumps(data))

        if response.status_code == 401:
            _logger.exception("Expired token found.")
            raise
        elif response.status_code==403:
            _logger.exception("Access Forbidden")
            raise
        elif response.status_code == 200:
            _logger.info("External model asset saved successfully")
            _logger.debug("External model asset saved successfully {}".format(response.json()))
        else:
            _logger.exception(
                "Error updating properties..{}".format(response.json()))
            raise


class ExternalModelSchemas:
    """
    External model schema

    :attr List[Dict] input: Model input data schema
    :attr List[Dict] output: (optional) Model output data schema

    """
    def __init__(self,input: List[Dict],
                output:List[Dict]=None) -> None:

        """
        Initialize a ExternalModelSchemas object.

        :param List[Dict] input: Model input data schema
        :param List[Dict] output: (optional) Model output data schema
        
        """

        self.input = input
        self.output = output

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ExternalModelSchemas':
        """Initialize a DeploymentDetails object from a json dictionary."""
        args = {}
        if 'input' in _dict:
            args['input'] = _dict.get('input')
        else:
            raise ValueError('Required property \'deployment_id\' not present in ExternalModelSchemas JSON')
        if 'output' in _dict:
            args['output'] = _dict.get('output') #[convert_model(x) for x in metrics]
        else:
            raise ValueError('Required property \'output\' not present in ExternalModelSchemas JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ExternalModelSchemas object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'input') and self.input is not None:
            _dict['input'] = self.input
        if hasattr(self, 'output') and self.output is not None:
            _dict['output'] = self.output
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ExternalModelSchemas object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ExternalModelSchemas') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ExternalModelSchemas') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class TrainingDataReference:
    """
    Training data schema definition

    :attr Dict schema: Model training data schema
    
    """
    def __init__(self,schema:Dict) -> None:
        """
        Initialize a TrainingDataReference object.

        :param Dict schema: Model training data schema
        
        """
        self.schema = schema

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'TrainingDataReference':
        """Initialize a TrainingDataReference object from a json dictionary."""
        args = {}
        if 'schema' in _dict:
            args['schema'] = _dict.get('schema')
        else:
            raise ValueError('Required property \'schema\' not present in TrainingDataReference JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a TrainingDataReference object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'schema') and self.schema is not None:
            _dict['schema'] = self.schema
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this TrainingDataReference object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'TrainingDataReference') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'TrainingDataReference') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeploymentDetails:
    """
    External model deployment details

    :attr str identifier: Deployment identifier specific to providers.
    :attr str name: Name of the deployment
    :attr str deployment_type: Deployment type (i.e., online)
    :attr str scoring_endpoint: Deployment scoring endpoint url.  
    
    """

    def __init__(self,identifier: str,
                 name: str,
                 deployment_type: str,
                 scoring_endpoint: str = None) -> None:
        
        """
        Initialize a DeploymentDetails object.

        :param str identifier: Deployment identifier specific to ML providers
        :param str name: Name of the deployment
        :param str deployment_type: Deployment type (i.e., online)
        :param str scoring_endpoint: Deployment scoring endpoint url.  

        """
        
        self.id = identifier
        self.name = name
        self.type = deployment_type
        self.scoring_endpoint = scoring_endpoint


    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeploymentDetails':
        """Initialize a DeploymentDetails object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        else:
            raise ValueError('Required property \'id\' not present in DeploymentDetails JSON')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in DeploymentDetails JSON')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        else:
            raise ValueError('Required property \'type\' not present in DeploymentDetails JSON')
        if 'scoring_endpoint' in _dict:
            args['scoring_endpoint'] = _dict.get('scoring_endpoint')
        else:
            raise ValueError('Required property \'scoring_endpoint\' not present in DeploymentDetails JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeploymentDetails object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'scoring_endpoint') and self.scoring_endpoint is not None:
            _dict['scoring_endpoint'] = self.scoring_endpoint
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeploymentDetails object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeploymentDetails') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeploymentDetails') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


