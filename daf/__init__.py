from flask import Flask
import json
import pprint 
import datetime
from flask import request
from daf_integration import *
import ast

    '''
    Dataset Param to pass:
      name
      theme
      subtheme
      org
      user 
      description
    '''
    def saveInDaf():
        if 'file' not in request.files:
            print('No file part')
        fileOriginal = request.files['file'].read()
        fileToUpload = fileOriginal
        originalKyloSchema = getKyloSchema(fileOriginal)
        kyloSchema = json.loads(originalKyloSchema)
        print(kyloSchema)
        fields = extractFields(kyloSchema)
        template = loadTemplate('./template_catalog.json')
        nameSingle = request.form['name'].replace(' ', '_')
        if not isPresentOnDaf(nameSingle):
            print('go forward')
            setDcatapit(template, request.form, nameSingle)
            setDataSchema(template, request.form, nameSingle, fields, originalKyloSchema)
            setOperational(template, request.form, nameSingle)
            created = createKyloFeed(template)
            if  created == 200:
                print('creating on mongo')
                catalogCreated = createMetacalog(template)
                print('created on mongo')
                if catalogCreated == 200:
                    print('saving on hdfs')
                    saveOrUpdateFile(fileToUpload, template)
                    print('saved on hdfs')
                    return json.dumps({'success' : "created"})
        return json.dumps({'error' : 'error'})
    return app
