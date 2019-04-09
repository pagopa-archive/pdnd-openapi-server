import time

import connexion
import six
from werkzeug.exceptions import Unauthorized
import requests
import json
from daf.daf_integration import saveInDaf
from flask import jsonify


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
    headers = {'Content-Type': 'application/json', 
               'Accept': 'application/json',
               'authorization': header}
    response = requests.request("GET", url, headers=headers)
    # response.text.replace('"','')
    #return {"jwt" : response.text}
    return jsonify({"jwt" : response.text.replace('"','')})

def basic_auth(username, password, required_scopes=None):
    print("ale")
    header = connexion.request.headers['Authorization']
    print(header)
    return  {'sub': 'user1', 'scope': ''}

def dataset_save(file):
    print(file)
    print(connexion.request.form)
    header = connexion.request.headers['Authorization']
    return saveInDaf(file,connexion.request.form, header)
    #return "ale"

def status():
    return {"status" : "ok"}

def dataset_save_test(file):
  header = connexion.request.headers['Authorization']
  url = 'https://api.daf.teamdigitale.it/hdfs/proxy/uploads/d_ale/GOVE/amministrazione/test_pdnd_api_9/test_pdnd_api_9_1554715519.csv?op=CREATE'
  print('URL')
  print(url)
  file.save('./tmp.csv')
  payload = open('./tmp.csv', 'rb').read()
  #payload = fileToUpload.read()
  headers = {
      'content-type': "text/csv",
      'authorization': header
      }
  response = requests.request("PUT", url, data=payload, headers=headers)
  if response.status_code == 200:
    return 200
  return 400


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, specification_dir='openapi/', options={"swagger_ui": True})
    app.add_api('daf-openapi.yaml') #, validate_responses=True)
    app.run(port=8080)
