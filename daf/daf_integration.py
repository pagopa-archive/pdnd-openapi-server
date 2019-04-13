import datetime
import json
import os
import time
from time import sleep
from shutil import copyfileobj
import copy

import requests

FLATSCHEMA_TEMPLATE = json.loads(
    """{
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
      }"""
)


def generateFlatSchema(fields, FLATSCHEMA_TEMPLATE):
    flatSchema = []
    for field in fields:
        FLATSCHEMA_TEMPLATE["name"] = field["name"]
        FLATSCHEMA_TEMPLATE["`type`"] = field["`type`"]
        flatSchema.append(FLATSCHEMA_TEMPLATE)
    return flatSchema


def isPresentOnDaf(name, header):
    isPresentUrl = (
        f"https://api.daf.teamdigitale.it/catalog-manager"
        "/v1/catalog-ds/is_present/{name}"
    )
    payload = ""
    headers = {"authorization": header}
    response = requests.request(
        "GET", isPresentUrl, data=payload, headers=headers
    )
    print(response.status_code)
    print(name)
    if response.status_code == 404:
        return False
    return True


def getKyloSchema(file, header, fileType="csv"):
    kyloInferUrl = (
        "https://api.daf.teamdigitale.it/dati-gov/v1/infer/kylo/csv"
    )
    if fileType == "json":
        kyloInferUrl = (
            "https://api.daf.teamdigitale.it/dati-gov/v1/infer/kylo/json"
        )
    headers = {"authorization": header}
    files = {"upfile": file}
    response = requests.post(kyloInferUrl, files=files, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    return {"error": "error"}


def createKyloFeed(metacatalog, header):
    startKyloUrl = (
        "https://api.daf.teamdigitale.it/catalog-manager/v1/kylo/feed/csv"
    )
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "authorization": header,
    }
    response = requests.post(
        startKyloUrl, data=json.dumps(metacatalog), headers=headers
    )
    if response.status_code == 200:
        # resp = json.loads(response.text)
        return 200
    return 400


def createMetacalog(metacatalog, header):
    startKyloUrl = (
        "https://api.daf.teamdigitale.it/catalog-manager/v1/catalog-ds/add"
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "authorization": header,
    }
    response = requests.post(
        startKyloUrl, data=json.dumps(metacatalog), headers=headers
    )
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        # resp = json.loads(response.text)
        return 200
    return 400


def startFeedJob(orgName, datasetName, header):
    starNifiUrl = (
        "https://api.daf.teamdigitale.it/catalog-manager/v1/nifi/start/"
        + orgName
        + "/"
        + datasetName
    )
    print(header)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": header,
    }
    response = requests.request("GET", starNifiUrl, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        return True
    return False


def saveOrUpdateFile(fileToUpload, metacatalog, header):
    genericUrl = metacatalog["operational"]["input_src"]["srv_push"][0]["url"]
    ts = str(int(time.time()))
    name = metacatalog["dcatapit"]["name"]
    url = genericUrl + name + "_" + ts + ".csv?op=CREATE"
    print("URL")
    print(url)
    payload = fileToUpload.read()
    headers = {"content-type": "text/csv", "authorization": header}
    response = requests.request("PUT", url, data=payload, headers=headers)
    if response.status_code == 200:
        return 200
    return 400



def extractFields(kyloSchema):
    fields = kyloSchema["fields"]
    newFields = map(
        lambda d: {"name": d["name"], "`type`": d["derivedDataType"]}, fields
    )
    return list(newFields)


def loadTemplate(pathTemplate):
    jsondata = open(pathTemplate).read()
    data = json.loads(jsondata)
    return data


def setDcatapit(template, form, nameSingle):
    modified = datetime.datetime.now().strftime("%d/%m/%Y")
    template["dcatapit"]["name"] = nameSingle
    template["dcatapit"]["title"] = form["name"]
    template["dcatapit"]["author"] = form["user"]
    template["dcatapit"]["alternate_identifier"] = form["name"]
    template["dcatapit"]["notes"] = form["description"]
    template["dcatapit"]["theme"] = form["theme"]
    template["dcatapit"]["publisher_name"] = form["org"]
    template["dcatapit"]["publisher_identifier"] = form["org"]
    template["dcatapit"]["holder_name"] = form["org"]
    template["dcatapit"]["holder_identifier"] = form["org"]
    template["dcatapit"]["organization"]["name"] = form["org"]
    template["dcatapit"]["owner_org"] = form["org"]
    template["dcatapit"]["modified"] = modified
    return template


def setDataSchema(template, form, nameSingle, fields, kyloSchema):
    template["dataschema"]["avro"][
        "namespace"
    ] = "daf://{org}/{theme}/{nameSingle}".format(
        org=form["org"], theme=form["theme"], nameSingle=nameSingle
    )
    template["dataschema"]["avro"]["name"] = nameSingle
    template["dataschema"]["avro"]["alliases"] = [nameSingle]
    template["dataschema"]["avro"]["fields"] = fields
    template["dataschema"]["kyloSchema"] = kyloSchema
    template["dataschema"]["flatSchema"] = generateFlatSchema(
        fields, FLATSCHEMA_TEMPLATE
    )
    return template


def setOperational(template, form, nameSingle):
    fileType = "csv"
    # if form['fileType'] is not None:
    #  fileType = form['fileType']
    template["operational"]["group_own"] = form["org"]
    template["operational"]["theme"] = form["theme"]
    template["operational"]["subtheme"] = form["subtheme"]
    template["operational"]["file_type"] = fileType
    template["operational"]["input_src"]["srv_push"][0]["username"] = form[
        "user"
    ]
    urlConvention = "/{user}/{theme}/{subtheme}/{nameSingle}/".format(
            user=form["user"],
            theme=form["theme"],
            subtheme=form["subtheme"],
            nameSingle=nameSingle,
    )
    template["operational"]["input_src"]["srv_push"][0]["url"] = \
        "https://api.daf.teamdigitale.it/hdfs/proxy/uploads" + urlConvention
    
    template["operational"]["input_src"]["srv_push"][0]["param"] = fileType
    return template


'''
Dataset Param to pass:
name
theme
subtheme
org
user
description
'''
def saveInDaf(fileToUpload,form,header):
        originalKyloSchema = getKyloSchema(fileToUpload,header)
        kyloSchema = json.loads(originalKyloSchema)
        #print(kyloSchema)
        fields = extractFields(kyloSchema)
        template = loadTemplate('./template_catalog.json')
        nameSingle = form['name'].replace(' ', '_')
        if not isPresentOnDaf(nameSingle, header):
            print('go forward')
            setDcatapit(template, form, nameSingle)
            setDataSchema(template, form, nameSingle, fields, originalKyloSchema)
            setOperational(template, form, nameSingle)
            #print(template)
            created = createKyloFeed(template, header)
            if  created == 200:
                print('creating on mongo')
                catalogCreated = createMetacalog(template, header)
                print('created on mongo')
                if catalogCreated == 200:
                    print('saving on hdfs')
                    fileToUpload.seek(0)
                    savedStatus = saveOrUpdateFile(fileToUpload, template, header) 
                    if savedStatus == 200:
                      return {'success' : "created"} 
        return {'error' : 'error'}
