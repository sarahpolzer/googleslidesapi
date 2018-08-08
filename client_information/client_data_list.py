#Importing required packages"

import requests
import json
import google_slides_functions
from google_slides_functions import create_presentation, duplicate_presentation

#This is the ID of the template presentation on Google Slides
template_id = "18y4Wz5NX5A-dCWxgbFka45akCoozSeojn0J7DUfLD00"
#I am requesting the 321 organizations API
rm = requests.get('https://my.321webmarketing.com/api/organizations')
organization_data = json.loads(rm.text)

#I am request the 321 what-converts API
Rm = requests.get('https://my.321webmarketing.com/api/what-converts')
what_converts_data = json.loads(Rm.text)

#I am defining a dictionary of Google Analytics data because this information is not publicly accessible

google_analytics = {'Fairfax Christ Lutheran Church' : '178504253',
                    'FVCbank' : '177043198',
                    'Insure My Drone': '177048086',
                    'MFE Insurance' : '172637218',
                    'Kangovou' : '149085017',
                    'Fairfax Mortgage Investments' : '161907510',
                    '321 Web Marketing': '89636352',
                    'Dirt Connections': '112999250',
                    'Presidential Heat and Air': '135116571',
                    'Paw Pals': '125525400',
                    'KPPB Law' : '149086333',
                    'Koncept Design + Build' : '149654643',
                    'The Brown Firm' : '103336963',
                    'Beyond Exteriors': '139537851',
                    'Business Benefits Group' : '119560347',
                    'Cobbdale Assisted Living': '126287032',
                     "Comfort Home Care": "80278574"}

org_logos = {'Fairfax Christ Lutheran Church' : "https://s27029.p370.sites.pressdns.com/wp-content/uploads/2018/04/celc-logo-white.png",
            "FVCbank" : "https://www.fvcbank.com/wp-content/uploads/2018/04/fvcbank-logo-larger.png",
            "Insure My Drone" : "https://insuremydrone.net/wp-content/uploads/2018/05/imd-logo.png",
            "Kangovou" : 'https://www.kangovou.com/wp-content/uploads/2016/08/Screen-Shot-2016-08-25-at-1.19.22-PM.png',
            'MFE Insurance' : "https://s26328.pcdn.co/wp-content/uploads/2018/03/mfe-logo-450x100.png"}

#what_converts = {'Comfort Home Care' : 
                 # 'Presidential Heat and Air' : 

#}





clients = {}

def make_client_dictionary():
    for item in organization_data:
        client_information = {}
        client = item['dba_name']
        client_information['domain_name'] = item['domain_name']
        client_information['org_logo'] = item['remote_logo_url']
        for what_converts in what_converts_data:
            if str(item['id']) in what_converts['organization']:
                client_information['what_converts'] = what_converts['account_id']
        presentation_id = duplicate_presentation(client, template_id)
        client_information['presentation_id'] = presentation_id
        clients[client] = client_information
    for clients_key in clients.keys():
        for google_key in google_analytics.keys():
            if clients_key == google_key:
                clients[clients_key]['google_analytics'] = google_analytics[google_key]
        for org_logo_key in org_logos.keys():
            if clients_key == org_logo_key and clients[clients_key]['org_logo'] is None:
                clients[clients_key]['org_logo'] = org_logos[org_logo_key] 
    with open('client_information.json', 'w') as outfile:
        return json.dump(clients, outfile)
        



make_client_dictionary()
