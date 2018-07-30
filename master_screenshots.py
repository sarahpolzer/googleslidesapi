#Importing required packages
import initialize_apis
from initialize_apis import get_slides_and_drive_apis
import os
from selenium import webdriver
from PIL import Image
from io import BytesIO
import google_slides_functions
from google_slides_functions import find_replace_img
from apiclient.http import MediaFileUpload
import json 
#The port which screenshots will be taken from 
port = 5004
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

#This function takes screenshots cropped images and returns an image url
def take_ss(url):
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    image_url = 'screenshot.png'
    driver.get(url)
    element = driver.find_element_by_tag_name("body")
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()
    driver.quit()
    im = Image.open(BytesIO(png))
    left = location['x']
    top= location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im= im.crop((left, top, right, bottom))
    im.save(image_url)
    return image_url

# This function posts the image, based on its url, on google drive, and then returns its new file id
def get_file_id(image_url):
    file_metadata = {'name': image_url,
    'parents': [folder_id]}
    media = MediaFileUpload(image_url, mimetype='image/jpeg', resumable = True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    return file_id

#This function gets the new file_id and turns it into a useable, global image link
def get_new_image_url(file_id):
    new_image_url = 'https://drive.google.com/uc?id=' + file_id
    return new_image_url


#This function removes the saved image
def delete_png_file(image_url):
    os.remove(image_url)


#This function removes the google drive file
def delete_google_drive_file(file_id):
    service = drive_service
    file_metadata = {'trashed':True}
    file = drive_service.files().update(body=file_metadata, fileId = file_id).execute()





#This function uses all of the functions above to effectively screenshot all of the urls in the
#url list and place the resulting images into specific shape/texts in the reports
def master(url_list):
    for url in url_list:
        url = 'http://127.0.0.1:' + str(port) + url
        image_url = take_ss(url)
        file_id = get_file_id(image_url)
        new_image_url = get_new_image_url(file_id)
        if 'traffic' in url:
            shape_text = '{{traffic}}'
            find_replace_img(pres_id, shape_text, new_image_url)
        elif 'leads' in url:
            shape_text = '{{leads}}'
            find_replace_img(pres_id, shape_text, new_image_url)
        elif 'report' in url:
            shape_text = '{{content_report_month}}'
            find_replace_img(pres_id, shape_text, new_image_url)
        else:
            shape_text= '{{content_next_month}}'
            find_replace_img(pres_id, shape_text, new_image_url)
        delete_png_file(image_url)
        delete_google_drive_file(file_id)

master(url_list)