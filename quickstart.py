"""
Shows basic usage of the Slides API. Prints the number of slides and elments in
a presentation.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools



# def create_presentation()
    # return presentation_id

# def create_slide()
    # return the slide and make sure it's hooked into the presentation

#def setup_googleslides_api():
    # Setup the Slides API
def setup_googleslides_api():
    SCOPES = 'https://www.googleapis.com/auth/presentations'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    slides_service = build('slides', 'v1', http=creds.authorize(Http()))
    return slides_service


def setup_googledrive_api():
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('credentialsdrive.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service
    # Call the Slides API
    #setup_googleslides_api()
#setup_googleslides_api()
setup_googledrive_api()
