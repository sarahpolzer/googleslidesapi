#python3.6
"""
functions to create a presentation, duplicate a presentation, find and replace strings, and find and replace
shapes to images using the Google Slides API

"""
#import function setup_googleslides_api
from quickstart import *
#import time packages
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
# getting the current time, which will be useful later when forming titles for slides

#A function to create a slides presentation with a given title, returning its presentation id
def create_presentation(title):
    service = setup_googleslides_api()
    body = { 
        'title': str(title)
    }
    presentation = service.presentations().create(body=body).execute()
    presentation_id = presentation.get('presentationId')
    return presentation_id

#A function to duplicate a presentation based off of a presentation id, returning the
#presentation id of the copy
def duplicate_presentation(presentation_id):
    service = setup_googledrive_api()
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
    service = setup_googleslides_api()
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
    service = setup_googleslides_api()
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

now = datetime.datetime.now()
month_before_last = now - relativedelta(months=1)
month_report = now + relativedelta(months=1)
next_month = month_report + relativedelta(months = 1)
pres_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
org = 'BBG'
org_website = 'www.bbgbroker.com'
org_logo = 'https://s16001.pcdn.co/wp-content/themes/kristie/images/updated-bbg-logo.png'
#slide 1

find_replace_str(pres_id, '{{mo_3l}}', month_report.strftime('%B '))
find_replace_str(pres_id, '{{year_4d}}', month_report.strftime('%Y'))

find_replace_str(pres_id, '{{org_website}}', org_website)

find_replace_img(pres_id, '{{org_logo}}', org_logo)


#slide 2
find_replace_str(pres_id, '{{nxt_mo}}', next_month.strftime('%B'))
find_replace_str(pres_id, '{{nxt_mo_year}}', next_month.strftime('%Y'))

#slide 3
find_replace_str(pres_id, '{{last_mo}}', now.strftime('%B'))
find_replace_str(pres_id, '{{last_mo_last_day}}', (now + relativedelta(day=31)).strftime('%d'))
find_replace_str(pres_id, '{{last_mo_year}}', "{}".format(now.year))
find_replace_str(pres_id, '{{org}}', 'BBG')

#slide 7
find_replace_str(pres_id, '{{mo_before_last}}', month_before_last.strftime('%B'))