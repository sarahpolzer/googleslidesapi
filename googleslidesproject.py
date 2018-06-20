#python3.6
"""
functions to create a presentation, create slides, duplicate slides, and find and replace elements in slides 
in the Google Slides API.

"""
#import function setup_googleslides_api
from quickstart import *
#import time packages
import time
import datetime

now = datetime.datetime.now()

def create_presentation(title):
    service = setup_googleslides_api()
    body = { 
        'title': str(title)
    }
    presentation = service.presentations().create(body=body).execute()
    presentation_id = presentation.get('presentationId')
    return presentation_id

#clients= []
#presentationids = []
#for client in clients:
    #create_presentation(client)
    #presentationids.append(presentation_id)



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

# define current date

# replace "june" with datetime.month function
#find_replace_slide('17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8', '{{mo_3l}}', 'June')
# replace year with current year
#find_replace_slide('17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8', '{{year_4d}}', '2018')
# replace with current client's website
#find_replace_slide('17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8', '{{org_website}}', 'www.bbgbroker.com')
    
#find_replace_img('17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8', '{{org_logo}}', 'https://pbs.twimg.com/profile_images/948761950363664385/Fpr2Oz35_400x400.jpg' )


#find_replace_str('17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8','{{year_4d}}', '{}'.format(now.year) )

find_replace_str('17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8', 'six', datetime.date.today().strftime("%B"))


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

presentationids = []
for client in clients:
    client = "{}".format(now.strftime('%m')) + client + " SEO BRIEFING" + now.strftime('%B')+ " {}". format(now.year)
    presentation_id = create_presentation(client)
    presentationids.append(presentation_id)




