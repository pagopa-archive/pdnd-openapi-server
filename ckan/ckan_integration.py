import json
import requests

def public_search(filters, headers):
    name = filters['text']
    #url = 'https://ckan-geo.daf.teamdigitale.it/api/3/action/resource_search?query=name:' + name 
    url = 'https://ckan.dev.pdnd.italia.it/api/3/action/resource_search?query=name:' + name
    print(url)
    r = requests.get(url)
    csvs = []
    if r.status_code == 200:
        result = r.json()['result']
        if result['count'] > 0:
            results = result['results']
            csvs = [{'name': x['name'], 'url': x['url']} for x in results if x['format'].lower() == 'csv']
    return csvs