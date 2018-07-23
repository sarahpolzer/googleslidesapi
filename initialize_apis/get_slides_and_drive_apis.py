"""
Shows basic usage of the Slides API. Prints the number of slides and elments in
a presentation.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials





def setup_googleslides_api():
    SCOPES = 'https://www.googleapis.com/auth/presentations'
    store = file.Storage('/Users/sarahpolzer/dev/googleslidesapi/credentials/credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/Users/sarahpolzer/dev/googleslidesapi/credentials/client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    slides_service = build('slides', 'v1', http=creds.authorize(Http()))
    return slides_service

    


def setup_googledrive_api():
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('/Users/sarahpolzer/dev/googleslidesapi/credentials/credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/Users/sarahpolzer/dev/googleslidesapi/credentials/service_account_creds.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service


def initialize_drive():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
  '/Users/sarahpolzer/dev/googleslidesapi/credentials/service_account_creds.json', 'https://www.googleapis.com/auth/drive.file')
  drive_service = build('drive', 'v3', credentials=credentials)
  return drive_service



initialize_drive()