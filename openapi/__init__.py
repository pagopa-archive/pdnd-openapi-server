import json

import connexion
import requests
from connexion import problem
from flask import jsonify

from daf.daf_integration import saveInDaf

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
    url = BASE_URL + "/dati-gov/v1/public/elasticsearch/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }  # 'Authorization': header}
    response = requests.post(
        url, data=json.dumps(filters["filters"]), headers=headers
    )
    return response.json()

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
        # response.text.replace('"','')
        # return {"jwt" : response.text}
        return jsonify({"jwt": response.text.replace('"', "")})
    # TODO log.error("Authentication error: %r", response.text)
    return problem(
        status=401,
        title="Authentication failed",
        detail="Not allowed by authorization server.",
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
