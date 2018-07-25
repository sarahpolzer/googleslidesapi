
#from quickstart import *
#import time packages
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import initialize_apis
import json
from initialize_apis import get_slides_and_drive_apis
from google_slides_functions import *

#pres_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
#org = 'BBG'
#org_website = 'www.bbgbroker.com'
#org_logo = 'https://s16001.pcdn.co/wp-content/themes/kristie/images/updated-bbg-logo.png'

#folder_id = '1hScQyb1uMLQaBmNgyHa1dlFZAO2mKzxC'
with open('client_information/client_information.json', 'r') as f:
     clients = json.load(f)
client = input('Who is the client? ')
org_website = clients[client]['domain_name'].replace("https://", "").replace("http://", "").replace('www/', 'www.')
org_logo = clients[client]['org_logo']
pres_id = clients[client]['presentation_id']
org = client

#Below functions are used to conduct search/replaces on elements in a Google Slides presentation
#constants
now = datetime.datetime.now()
month_current = now
month_previous = now - relativedelta(months=1)
month_next = now + relativedelta(months=1)
mo_3l = month_current.strftime('%B')
year_4d = month_current.strftime('%Y')
mo_nxt = month_next.strftime('%B')
year_nxt_mo= month_next.strftime('%Y')
mo_last = month_previous.strftime('%B')
day_last_last_mo = (month_previous + relativedelta(day=31)).strftime('%d')
year_last_mo = month_previous.strftime('%Y')
month_before_last = month_previous - relativedelta(months=1)
mo_before_last = month_before_last.strftime('%B')

#slide 1 search replace

find_replace_str(pres_id, '{{mo_3l}}', mo_3l)
find_replace_str(pres_id, '{{year_4d}}', year_4d)
find_replace_str(pres_id, '{{org_website}}', org_website)
find_replace_img(pres_id, '{{org_logo}}', org_logo)

#slide 2 search replace
find_replace_str(pres_id, '{{mo_nxt}}', mo_nxt)
find_replace_str(pres_id, '{{year_nxt_mo}}', year_nxt_mo)

#slide 3 search replace
find_replace_str(pres_id, '{{mo_last}}', mo_last)
find_replace_str(pres_id, '{{day_last_last_mo}}', day_last_last_mo)
find_replace_str(pres_id, '{{year_last_mo}}', year_last_mo)
find_replace_str(pres_id, '{{org}}', org)


#slide 7 search replace
find_replace_str(pres_id, '{{mo_before_last}}', mo_before_last)  

