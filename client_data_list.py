#This is going to be sudo code
#What I need in this list is...
# organization name, organization logo, presentation-Id for their report, their View-Id for google analytics, their domain
# name, and their account id for what converts.

import requests
import json 

rm = requests.get('https://my.321webmarketing.com/api/organizations')
json_data = json.loads(rm.text)
print(json_data['dba_name'])
with open('client_list.json', 'w') as outfile:
    json.dump(json_data, outfile)