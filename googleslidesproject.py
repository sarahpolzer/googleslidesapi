#python3.6
"""
functions to create a presentation, duplicate a presentation, find and replace strings, and find and replace
shapes to images using the Google Slides API

"""

#from quickstart import *
#import time packages
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import initialize_apis
from initialize_apis import get_slides_and_drive_apis
#from get_slides_and_drive_apis import setup_googleslides_api, setup_googledrive_api
slides_service = get_slides_and_drive_apis.setup_googleslides_api()
drive_service =  get_slides_and_drive_apis.setup_googledrive_api()
# getting the current time, which will be useful later when forming titles for slides

#A function to create a slides presentation with a given title, returning its presentation id
def create_presentation(title):
    service = slides_service
    body = { 
        'title': str(title)
    }
    presentation = service.presentations().create(body=body).execute()
    presentation_id = presentation.get('presentationId')
    return presentation_id

#A function to duplicate a presentation based off of a presentation id, returning the
#presentation id of the copy
def duplicate_presentation(presentation_id):
    service = drive_service
    body = {
        'name': 'copy'
    }
    drive_response = service.files().copy(
        fileId = str(presentation_id), body=body).execute()
    presentation_copy_id = drive_response.get('id')
    print(presentation_copy_id)
    return presentation_copy_id
    

 #A function to conduct a find and replace for strings in a presentation with a given id   
def find_replace_str(slides_id, before_str, after_str):
    service = slides_service
    body =  {
        "requests" : [
            {
            "replaceAllText" : {
                "containsText" : {
                    "text" : before_str,
                    "matchCase" : False
                },
               # "pageObjectIds": [
                   # "1" ],
                "replaceText": after_str

            }

            }  
            ] 
         }
   
    response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()


#A function to conduct a find and replace, replacing a shape with a specific word in it
#with an image in a presentation with a given id
def find_replace_img(slides_id, shape_text, new_img_url):
    service = slides_service
    body = {
        "requests": [
        {
            "replaceAllShapesWithImage":{
            "imageUrl" : new_img_url,
            "containsText":{
                "text": shape_text,
                "matchCase":False
                 }
            }
        }
    ]
    }
    response = service.presentations().batchUpdate(presentationId = slides_id, body = body).execute()
#Below functions are used to conduct search/replaces on elements in a Google Slides presentation
#constants
now = datetime.datetime.now()
month_current = now
month_previous = now - relativedelta(months=1)
month_next = now + relativedelta(months=1)
pres_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
org = 'BBG'
org_website = 'www.bbgbroker.com'
org_logo = 'https://s16001.pcdn.co/wp-content/themes/kristie/images/updated-bbg-logo.png'


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