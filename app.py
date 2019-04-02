import time

import connexion
import six
from werkzeug.exceptions import Unauthorized
import requests
import json

def forward_token(token):
    return  {'sub': 'user1', 'scope': ''}

def public_data_search(**filters):
    url = "https://api.daf.teamdigitale.it/dati-gov/v1/public/elasticsearch/search"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'} #'Authorization': header}
    print(filters['filters'])
    response = requests.post(url, data=json.dumps(filters['filters']), headers=headers)
    print(response.json())
    return response.json()

def get_token():
    header = connexion.request.headers['Authorization']
    url = "https://api.daf.teamdigitale.it/security-manager/v1/token"
    headers = {'authorization': header}
    response = requests.request("GET", url, headers=headers)
    return response.text

def basic_auth(username, password, required_scopes=None):
    print("ale")
    header = connexion.request.headers['Authorization']
    print(header)
    return  {'sub': 'user1', 'scope': ''}


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__)# specification_dir='openapi/', options={"swagger_ui": True})
    app.add_api('daf-openapi.yaml')
    app.run(port=8080)
