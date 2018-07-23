#This is going to be sudo code
#What I need in this list is...
# organization name, organization logo, presentation-Id for their report, their View-Id for google analytics, their domain
# name, and their account id for what converts.

import requests
import json 
import googleslidesproject
from googleslidesproject import create_presentation, duplicate_presentation

template_id = '1I5_dqdlr04hLboemHHRniffcMeZ9pc2bSpDffxMLmtE'


rm = requests.get('https://my.321webmarketing.com/api/organizations')
organization_data = json.loads(rm.text)
#with open('organization_list.json', 'w') as outfile:
  #  json.dump(organization_data, outfile)


Rm = requests.get('https://my.321webmarketing.com/api/what-converts')
what_converts_data = json.loads(Rm.text)
#with open('what_converts_list.json', 'w') as outfile:
   # json.dump(what_converts_data, outfile)


clients = {}

def make_client_dictionary():
    for item in organization_data:
        client_information = {}
        client = item['dba_name']
        client_information['domain_name'] = item['dba_name']
        client_information['org_logo'] = item['remote_logo_url']
        for what_converts in what_converts_data:
            if str(item['id']) in what_converts['organization']:
                client_information['what_converts'] = what_converts['account_id']
        presentation_id = duplicate_presentation(client, template_id)
        client_information['presentation_id'] = presentation_id
        clients[client] = client_information
    with open('client_information.json', 'w') as outfile:
        return json.dump(clients, outfile)


make_client_dictionary()