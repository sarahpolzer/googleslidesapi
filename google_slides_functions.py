#python3.6
"""
functions to create a presentation, duplicate a presentation, find and replace strings, and find and replace
shapes to images using the Google Slides API

"""

#from quickstart import *
#import time packages
import initialize_apis
from initialize_apis import get_slides_and_drive_apis
#from get_slides_and_drive_apis import setup_googleslides_api, setup_googledrive_api
slides_service = get_slides_and_drive_apis.setup_googleslides_api()
drive_service =  get_slides_and_drive_apis.setup_googledrive_api()
drive_service_two = get_slides_and_drive_apis.initialize_drive()



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
def duplicate_presentation(name, presentation_id):
    service = drive_service
    body = {
        'name': name
    }
    drive_response = service.files().copy(
        fileId = presentation_id, body=body).execute()
    presentation_copy_id = drive_response.get('id')
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


