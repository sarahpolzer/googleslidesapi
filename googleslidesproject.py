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
# getting the current time, which will be useful later when forming titles for slides
now = datetime.datetime.now()

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




#A list of current clients
clients = ['321 Web Marketing',
                'BBG',
                'Beyond Exteriors',
                'Brown Firm',
                'Dirt Connections',
                'Fairfax Christ Lutheran',
                'FMI',
                'FVCbank',
                'Insure My Drone',
                 'Kangovou',
                 'KPPB Law',
                 'MFE Insurance',
                 'Paw Pals',
                 'SmartHR',
                'Comfort Home Care',
                 'Presidential Heat and Air']

#A for loop to create a presentation for each client with a title formatted ({MM}){Client} SEO Briefing {Month} {Year} (
presentationids = []
for client in clients:
    client = "{}".format(now.strftime('%m')) + client + " SEO BRIEFING " + now.strftime('%B')+ " {}". format(now.year)
    presentation_id = create_presentation(client)
    presentationids.append(presentation_id)



