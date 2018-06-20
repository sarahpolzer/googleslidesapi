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
        'title': title
    }
    presentation = service.presentations().create(body=body).execute()
    presentation_id = presentation.get('presentation_id')
    return presentation_id


#Create a new slide in presentation and return slide ID
def create_slide(presentation_id):
    service = setup_googleslides_api()
    page_id = '123456'    
    requests = [
        {
            'createSlide': {
                'objectId': page_id,
                'insertionIndex': '1',
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                }
            }
        }
    ]
    body = {
        'requests': requests
    }
    response = service.presentations().batchUpdate(presentation_id=presentation_id,
                                                            body=body).execute()
    create_slide_response = response.get('replies')[0].get('createSlide')
    slide_id = create_slide_response.get('objectId')
    return slide_id

#Duplicate a slide in a presentation and return the new slide id
def duplicate_slide(presentation_id,slide_id):
    service = setup_googleslides_api()
    requests = [
        {
            "duplicateObject":{
                'objectId': slide_id,
                'objectIds': {
                    str(slide_id) : "copiedSlide_001"
            }
            }
        }
    
    ]
    body = {
        'requests' : requests
    }
    response = service.presentations().batchUpdate(presentation_id = presentation_id,
                                                    body = body).execute()
    create_slide_response = response.get('replies')[0].get('duplicateObject')
    new_slide_id = create_slide_response.get("slide_id")
    return new_slide_id

#find and replace strings from a slide-id
def find_replace_slide(presentation_id, new_slide_id, before_str, after_str):
    service = setup_googleslides_api()
    requests = [
        { 
            {"replaceAllText" :{
             'objectId': slide_id, 
            {"findText" : before_str, 'replaceText':after_str} }
                
            }
        }
     ]
    body = {
        'requests': requests
    }
    response = service.presentations().batchUpdate(presentation_id = presentation_id,
                                                    body = body).execute()
    create_slide_response = response.get('replies')[0].get('ReplaceAllTextRequest')



def test(title):
    presentation_id = create_presentation(title)
    slideId = create_slide(presentation_id)
    new_slide = duplicate_slide(presentation_id, slideId)
    find_replace_slide(presentation_id, new_slide, 'Title', 'Yam')


test('Yams')