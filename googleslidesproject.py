#python3.6
"""
functions to create a presentation, create slides, duplicate slides, and find and replace elements in slides 
in the Google Slides API.

"""
#import function setup_googleslides_api
from quickstart import *

#create a new presentation and return  its presentation id
def create_presentation(title):
    service = setup_googleslides_api()
    body = { 
        'title': str(title)
    }
    presentation = service.presentations().create(body=body).execute()
    presentation_id = presentation.get('presentationId')
    print(presentation_id)
    return presentation_id

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
    
    
def find_replace_slide(presentation_copy_id, before_str, after_str):
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
   
    response = service.presentations().batchUpdate(presentationId = presentation_copy_id, body = body).execute()


  



    
    







