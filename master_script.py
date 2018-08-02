
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
from find_client_options import find_clients_options
from find_client_options import convert_number_to_client
#Service for google slides API
slides_service = get_slides_and_drive_apis.setup_googleslides_api()
#Service for google drive API
drive_service =  get_slides_and_drive_apis.initialize_drive()
"""variables for flask screenshots"""
#The port which screenshots will be taken from 
port = 5005
#The list of urls that will be screenshotted
url_list = ['/traffic', '/leads']

"""Variables for uploading flask and ahrefs screenshots into Google Drive API"""
#Folder in which I have permissions to put files into my drive and remove them
folder_id = '1hScQyb1uMLQaBmNgyHa1dlFZAO2mKzxC'
page_id = 'g202ad04c01_0_6'


"""Reading client data so that functions are performed on correct report"""
with open('client_information/client_information.json', 'r') as f:
    clients = json.load(f)
"""displaying clients with reports assigned to numbers for the User to select """
clients_option = find_clients_options(clients)
"""asking User who the client is"""
client = input(clients_option)
"""converting the number that the User inputs to the client it represented"""
client = convert_number_to_client(clients, client)

"""Important variables for ahrefs scrape. The ahrefs scrape master function has a lot of arguments"""
domains_image = 'domains_count.png' #file that the domains ahrefs screenshot will be saved in
keywords_image = 'keyword_count.png' #file that the keywords ahrefs screenshot will be saved in 
images = [domains_image, keywords_image] #A list of these image urls to later loop through
ahrefs_pw = os.environ['AHREFS_PW'] #ahrefs password
ahrefs_un = os.environ['AHREFS_UN'] #ahrefs username
domain_name = clients[client]['domain_name'].replace("https://", "").replace("http://", "").replace('www/', 'www.')
#client domain name that will be used to scrape the correct ahrefs page

#This is the main function that ties it all together
def main():
    extraneous_find_and_replace_master(clients,client)
    flask_screenshots_master(clients, client, url_list, port, folder_id, drive_service)
    ahrefs_scrape_master(clients, client, domains_image, keywords_image, images, ahrefs_un, ahrefs_pw, folder_id, drive_service)
    



main()