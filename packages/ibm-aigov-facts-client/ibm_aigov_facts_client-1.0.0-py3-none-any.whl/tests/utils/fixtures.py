import pytest
import os
import json
import time
import shutil
from datetime import datetime, timezone


from ibm_aigov_facts_client import AIGovFactsClient
from tests.utils.credentials import get_facts_client_credentials


class GlobalVars:
    pass


@pytest.fixture(scope='session')
def facts_client_credentials():
    return get_facts_client_credentials()


@pytest.fixture(scope='session')
def remove_folder(path):
    # check if folder exists
    if os.path.exists(path):
        # remove if exists
        shutil.rmtree(path)
