
import json  
import initialize_apis
from initialize_apis import get_slides_and_drive_apis
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import google_slides_functions
from google_slides_functions import find_replace_img, find_replace_str
from apiclient.http import MediaFileUpload
from time import sleep
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from ahrefs_scrape import ahrefs_scrape_master
from flask_screenshots import flask_screenshots_master
from extraneous_find_and_replace import extraneous_find_and_replace_master
#The port which screenshots will be taken from 
port = 5005
#The list of urls that will be screenshotted
url_list = ['/traffic', '/leads', '/content_report_month', '/content_next_month']

#service for google slides API
slides_service = get_slides_and_drive_apis.setup_googleslides_api()

#service for google drive API 
drive_service =  get_slides_and_drive_apis.initialize_drive()

#Folder in which I have permissions to put files into my drive and remove them
folder_id = '1hScQyb1uMLQaBmNgyHa1dlFZAO2mKzxC'

#I have no recollection of what this variable is.
page_id = 'g202ad04c01_0_6'

#Reading JSON File so that the screenshots are found/replaced into the appropriate presentation for the
#client
with open('client_information/client_information.json', 'r') as f:
    clients = json.load(f)
#Asking User who the client is
client = input('Who is the client? ')

#Determining presentation ID
pres_id = clients[client]['presentation_id']

#Important variables for ahrefs scrape
referring_domains = '{{domains}}'
referring_pages = '{{pages}}'
org_keywords = '{{org_keywords}}'
domains_image = 'domains_count.png'
keywords_image = 'keyword_count.png'
images = [domains_image, keywords_image]
ahrefs_pw = os.environ['AHREFS_PW']
ahrefs_un = os.environ['AHREFS_UN']
domain_name = clients[client]['domain_name'].replace("https://", "").replace("http://", "").replace('www/', 'www.')

#This is the main function that ties it all together
def main():
    extraneous_find_and_replace_master(clients,client)
    flask_screenshots_master(clients, client, url_list, port, folder_id, drive_service)
    ahrefs_scrape_master(clients, client, referring_domains, referring_pages, org_keywords, domains_image, keywords_image, images, ahrefs_un, ahrefs_pw, folder_id, drive_service)
    



main()