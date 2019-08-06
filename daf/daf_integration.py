import json

import connexion
import requests
from connexion import problem
from flask import jsonify

from daf.daf_save_dataset import saveInDaf

BASE_URL = "https://api.daf.teamdigitale.it"

def search_dataset(filters, headers):
    """Search for a dataset as search for keywords in document.

    See openapi file for a working example and parameter passes

    :param filters:
    :return:
    """

    url = BASE_URL + "/dati-gov/v1/public/elasticsearch/search"
    response = requests.post(
        url, data=json.dumps(filters), headers=headers
    )
    return response.json()