import json
import requests

def public_search(filters, headers):
    name = filters['text']
    #url = 'https://ckan-geo.daf.teamdigitale.it/api/3/action/resource_search?query=name:' + name 
    #url = 'https://ckan.dev.pdnd.italia.it/api/3/action/resource_search?query=name:' + name
    url = 'https://catalog.data.gov/api/3/action/package_search?q=' + name
    print(url)
    r = requests.get(url)
    csvs = []
    if r.status_code == 200:
        result = r.json()['result']
        if result['count'] > 0:
            print(result['count'])
            results = result['results']
            # only for  data.gov
            for res in results:
                resources = res['resources']
                name = res['title']
                csv = [{'name': name, 'url': x['url']} for x in resources if x['format'].lower() == 'csv']
                for info in csv:
                    csvs.append(info)
    return csvs