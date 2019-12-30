import json

import connexion
import requests
from connexion import problem
from flask import jsonify

from daf.daf_save_dataset import saveInDaf
from daf.daf_integration import *
from ckan.ckan_integration import public_search

from .util import loggable

BASE_URL = "https://api.daf.teamdigitale.it"


def forward_token(token):
    return {"sub": "user1", "scope": ""}

@loggable
def public_data_search(**filters):
    """Search for a dataset as search for keywords in document.

    See openapi file for a working example and parameter passes

    :param filters:
    :return:
    """
    #url = BASE_URL + "/dati-gov/v1/public/elasticsearch/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }  # 'Authorization': header}
    public_search(filters["filters"],headers)
    return search_dataset(filters["filters"],headers)

@loggable
def get_token():
    """Forwards an authentication request to the daf backend.

    :return:
    """
    backend_url = BASE_URL + "/security-manager/v1/token"
    header = connexion.request.headers["Authorization"]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "authorization": header,
    }
    response = requests.request("GET", backend_url, headers=headers)

    if response.status_code == 200:
        return jsonify({"jwt": response.text.replace('"', "")})
    # TODO log.error("Authentication error: %r", response.text)
    return problem(
        status=401,
        title="Authentication failed",
        detail="Not allowed by authorization server.",
    )

@loggable
def dataset_by_name(name):
    """Search dataset by name

    :return:
    {"name": metacatalog['dcatapit']['name'],
    "logical_uri": metacatalog['operational']['logical_uri'],
    "physical_uri": metacatalog['operational']['physical_uri'],
    "isExtOpenData": 'ext_opendata' in metacatalog['operational']}
    """
    backend_url = BASE_URL + "/catalog-manager/v1/public/catalog-ds/getbyname/" + name
    header = connexion.request.headers["Authorization"]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "authorization": header,
    }
    response = requests.request("GET", backend_url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        # response.text.replace('"','')
        # return {"jwt" : response.text}
        metacatalog = response.json()
        print(json.dumps(response.json(), indent=4, sort_keys=True))
        return jsonify({
            "name": metacatalog['dcatapit']['name'],
            "logical_uri": metacatalog['operational']['logical_uri'],
            "physical_uri": metacatalog['operational']['physical_uri'],\
            "isExtOpenData": 'ext_opendata' in metacatalog['operational']
        })
    # TODO log.error("Authentication error: %r", response.text)
    elif response.status_code == 401:
        return problem(
            status=401,
            title="Authentication failed",
            detail="Not allowed by authorization server.",
        )
    else:
        return problem(
            status=404,
            title="Url not found",
            detail="The dataset not found on pdnd",
        )   


def basic_auth(username, password, required_scopes=None):
    """Authenticates connexion requests as specified in the docs.

    See https://github.com/zalando/connexion/blob/master/docs/security.rst

    :param username:
    :param password:
    :param required_scopes:
    :return:
    """
    header = connexion.request.headers["Authorization"]
    print(header)
    return {"sub": "user1", "scope": ""}

@loggable
def dataset_save(file):
    """Save or update a dataset into PNDN.

    See swagger example for object passed via multipart/form

    :param file:
    :return:
    """
    header = connexion.request.headers["Authorization"]
    return saveInDaf(file, connexion.request.form, header)
    # return "ale"

@loggable
def status():
    return problem(
        status=200, title="OK", detail="Application is working normally"
    )

@loggable
def pdnd_search(**filters):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        return search_dataset(filters, headers)

@loggable
def pdnd_search_ckan(**filters):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        return public_search(filters["filters"],headers)