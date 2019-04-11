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


def public_data_search(**filters):
    url = f"{BASE_URL}/dati-gov/v1/public/elasticsearch/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }  # 'Authorization': header}
    print(filters["filters"])
    response = requests.post(
        url, data=json.dumps(filters["filters"]), headers=headers
    )
    print(response.json())
    return response.json()


def get_token():
    """Forwards an authentication request to the daf backend.

    :return:
    """
    backend_url = f"{BASE_URL}/security-manager/v1/token"
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


@loggable
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


def dataset_save(file):
    print(file)
    print(connexion.request.form)
    header = connexion.request.headers["Authorization"]
    return saveInDaf(file, connexion.request.form, header)
    # return "ale"


def status():
    return problem(
        status=200, title="OK", detail="Application is working normally"
    )


def dataset_save_test(file):
    header = connexion.request.headers["Authorization"]
    url = (
        f"{BASE_URL}/hdfs/proxy/uploads/"
        "d_ale/GOVE/amministrazione/test_pdnd_api_9/"
        "test_pdnd_api_9_1554715519.csv?op=CREATE"
    )
    print("URL")
    print(url)
    file.save("./tmp.csv")
    payload = open("./tmp.csv", "rb").read()
    # payload = fileToUpload.read()
    headers = {"content-type": "text/csv", "authorization": header}
    response = requests.request("PUT", url, data=payload, headers=headers)
    if response.status_code == 200:
        return 200
    return 400
