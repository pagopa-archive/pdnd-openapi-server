import requests
import json
import time
import datetime


FLATSCHEMA_TEMPLATE = json.loads("""{
        "name": "id",
        "`type`": "int",
        "metadata": {
          "type": "int",
          "desc": "",
          "tag": [],
          "format_std": {
            "conv": []
          },
          "semantics": {
            "id": ""
          },
          "field_profile": {},
          "personal": {}
        }
      }""")

def generateFlatSchema(fields, FLATSCHEMA_TEMPLATE):
    flatSchema = []
    for field in fields:
        FLATSCHEMA_TEMPLATE['name'] = field['name']
        FLATSCHEMA_TEMPLATE['`type`'] = field['`type`']
        flatSchema.append(FLATSCHEMA_TEMPLATE)
    return flatSchema

def isPresentOnDaf(name):
    isPresentUrl = "http://localhost:9001/catalog-manager/v1/catalog-ds/is_present/" + name
    payload = ""
    headers = {'authorization': 'Basic XXXXXXXXXX'}
    response = requests.request("GET", isPresentUrl, data=payload, headers=headers)
    print(response.status_code)
    print(name)
    if response.status_code == 404:
       return False
    return True


def getKyloSchema(file, fileType = 'csv'):
    kyloInferUrl = "https://api.daf.teamdigitale.it/dati-gov/v1/infer/kylo/csv"
    if fileType == 'json':
       kyloInferUrl = "https://api.daf.teamdigitale.it/dati-gov/v1/infer/kylo/json"
    headers = {'authorization': 'Basic XXXXXXXXXX'}
    files = {'upfile': file}
    response = requests.post(kyloInferUrl, files=files, headers=headers)
    print(response.status_code)
    #print(response.body)
    if response.status_code == 200:
       #resp = json.loads(response.text)
       return json.loads(response.text)
    return {"error" : "error"}

def createKyloFeed(metacatalog):
    startKyloUrl = "https://api.daf.teamdigitale.it/catalog-manager/v1/kylo/feed/csv"
    payload = ""
    headers = {
      'content-type': 'application/json', 
      'accept': 'application/json',
      'authorization': 'Basic XXXXXXXXXX'
    }
    print(json.dumps(metacatalog))
    response = requests.post(startKyloUrl, data=json.dumps(metacatalog), headers=headers)
    print("QUI CI SONO")
    print(response.status_code)
    #print(response.text)
    if response.status_code == 200:
       #resp = json.loads(response.text)
       return 200
    return 400

def createMetacalog(metacatalog):
    startKyloUrl = "https://api.daf.teamdigitale.it/catalog-manager/v1/catalog-ds/add"
    headers = {
      'Content-Type': 'application/json', 
      'Accept': 'application/json',
      'authorization': 'Basic XXXXXXXXXX'
      }
    response = requests.post(startKyloUrl, data=json.dumps(metacatalog), headers=headers)
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
       #resp = json.loads(response.text)
       return 200
    return 400

def saveOrUpdateFile(file, metacatalog):
  #url = "https://api.daf.teamdigitale.it/hdfs/proxy/uploads/d_ale/GOVE/amministrazione/anpr_previsioni_grezze_test/anpr_raw_forecast_18_months_28102018_182850.csv?op=CREATE"
  genericUrl = metacatalog['operational']['input_src']['srv_push'][0]['url']
  ts = str(int(time.time()))
  name = metacatalog['dcatapit']['name']
  url = genericUrl + name + '_' + ts + '.csv?op=CREATE'
  print('URL')
  print(url)
  payload = file
  headers = {
      'content-type': "text/csv",
      'authorization': "Basic XXXXXXXXXX"
      }
  response = requests.request("PUT", url, data=payload, headers=headers)
  if response.status_code == 200:
    return 200
  return 400
  #print(response.text)

def extractFields(kyloSchema):
    fields = kyloSchema['fields']
    newFields = map(lambda d: {"name" : d['name'], "`type`" : d['derivedDataType']}, fields)
    return newFields

def loadTemplate(pathTemplate):
    jsondata=open(pathTemplate).read()
    data = json.loads(jsondata)
    return data

def setDcatapit(template, form, nameSingle):
    modified = datetime.datetime.now().strftime("%d/%m/%Y") 
    template['dcatapit']['name'] = nameSingle
    template['dcatapit']['title'] = form['name']
    template['dcatapit']['author'] = form['user']
    template['dcatapit']['alternate_identifier'] = form['name']
    template['dcatapit']['notes'] = form['description']
    template['dcatapit']['theme'] = form['theme']
    template['dcatapit']['publisher_name'] = form['org']
    template['dcatapit']['publisher_identifier'] = form['org']
    template['dcatapit']['holder_name'] = form['org']
    template['dcatapit']['holder_identifier'] = form['org']
    template['dcatapit']["organization"]['name'] = form['org']
    template['dcatapit']['owner_org'] = form['org']
    template['dcatapit']['modified'] = modified
    return template

def setDataSchema(template, form, nameSingle, fields, kyloSchema):
    template['dataschema']['avro']['namespace'] = 'daf://{org}/{theme}/{nameSingle}' \
        .format(org=form['org'],theme=form['theme'], nameSingle=nameSingle )
    template['dataschema']['avro']['name'] = nameSingle
    template['dataschema']['avro']['alliases'] = [nameSingle]
    template['dataschema']['avro']['fields'] = fields
    template['dataschema']['kyloSchema'] = kyloSchema
    template['dataschema']['flatSchema'] = generateFlatSchema(fields,FLATSCHEMA_TEMPLATE)
    return template

def setOperational(template, form, nameSingle):
    fileType = 'csv'
    if form['fileType'] is not None:
      fileType = form['fileType']
    template['operational']['group_own'] = form['org']
    template['operational']['theme'] = form['theme']
    template['operational']['subtheme'] = form['subtheme']
    template['operational']['file_type'] = fileType
    template['operational']['input_src']['srv_push'][0]['username'] = form['user']
    template['operational']['input_src']['srv_push'][0]['url'] = \
        'https://api.daf.teamdigitale.it/hdfs/proxy/uploads/{user}/{theme}/{subtheme}/{nameSingle}/' \
            .format(user=form['user'],theme=form['theme'],subtheme=form['subtheme'],nameSingle=nameSingle)
    template['operational']['input_src']['srv_push'][0]['param'] = fileType
    return template


