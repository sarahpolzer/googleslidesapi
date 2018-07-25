
import initialize_apis
from initialize_apis import get_slides_and_drive_apis
import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from PIL import Image
slides_service = get_slides_and_drive_apis.setup_googleslides_api()
drive_service =  get_slides_and_drive_apis.initialize_drive()
import google_slides_functions
from google_slides_functions import find_replace_img
from apiclient.http import MediaFileUpload
import json 
#don't forget to add your environmental variables
ahrefs_pw = os.environ['AHREFS_PW']
ahrefs_un = os.environ['AHREFS_UN']
#domain_name = 'kppblaw.com'
with open('client_information/client_information.json', 'r') as f:
     clients = json.load(f)
client = input('Who is the client? ')
domain_name = clients[client]['domain_name'].replace("https://", "").replace("http://", "").replace('www/', 'www.')
pres_id = clients[client]['presentation_id']
folder_id = '1hScQyb1uMLQaBmNgyHa1dlFZAO2mKzxC'
page_id = 'g202ad04c01_0_6'


domains_image = 'domains_count.png'
keywords_image = 'keyword_count.png'
images = [domains_image, keywords_image] #A list that will be used later on in master function


#A function to take screenshots of domains and keywords charts from ahrefs
def take_ahrefs_screenshots():
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(10) # seconds
    driver.get("https://ahrefs.com/user/login/")
    #assert "Ahrefs" in driver.title
    elem = driver.find_element_by_id("email_input")
    elem.send_keys(ahrefs_un)
    elem = driver.find_element_by_name("password")
    elem.send_keys(ahrefs_pw)
    driver.find_element_by_css_selector('input.btn').click()
    sleep(2)
    driver.implicitly_wait(10) # seconds
    driver.get("https://ahrefs.com/site-explorer/overview/v2/subdomains/fresh?target=" + domain_name)
    sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 8);")
    driver.save_screenshot(domains_image)
    driver.find_element_by_xpath('//li[@name="se-overview-tabs"][2]/a').click()
    sleep(15)
    driver.implicitly_wait(10) # seconds
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 8);")
    driver.save_screenshot(keywords_image)
    driver.close()

#A function to crop the domains image so that it only contains the necessary charts for the reports
def crop_domains_image(domains_image):
    img = Image.open(domains_image)
    img = img.crop((199,202,935,763))
    img.save(domains_image)
    return domains_image    

#A function to crop the keywords image so that it only contains the necessary chart for the reports
def crop_keywords_image(keywords_image):
    img = Image.open(keywords_image)
    img = img.crop((208,408,937,670))
    img.save(keywords_image)
    return keywords_image

#A function to upload the new image to Google Drive, and then return its file id. This file will later be
#used to generate a image url.
def get_file_id(image_url):
    file_metadata = {'name': image_url,
    'parents': [folder_id]}
    media = MediaFileUpload(image_url, mimetype='image/jpeg', resumable = True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    return file_id

#A function to get the new images url
def get_new_image_url(file_id):
    new_image_url = 'https://drive.google.com/uc?id=' + file_id
    return new_image_url

#a function to delete the image files
def delete_png_file(image_url):
    os.remove(image_url)


#A function to delete the google drive file that is created by the get_file_id function
def delete_google_drive_file(file_id):
    service = drive_service
    file_metadata = {'trashed':True}
    file = drive_service.files().update(body=file_metadata, fileId = file_id).execute()

#This function takes the ahrefs screenshots and then crops the images. I would recommend running it sparingly
#as it is frowned upon to crawl ahrefs.
def take_screenshots_and_crop_images():
     take_ahrefs_screenshots()
     crop_domains_image(domains_image)
     crop_keywords_image(keywords_image)
     images = [domains_image, keywords_image]
     return images
#The master function where the images  will be inserted into the reports
def find_and_replace_ahrefs_images_into_reports(images):
    for image in images:
        file_id = get_file_id(image)
        new_image_url = get_new_image_url(file_id)
        if 'domains' in image:
            find_replace_img(pres_id, '{{domains_chart}}', new_image_url)
        else:
            find_replace_img(pres_id, '{{keywords_chart}}', new_image_url)
        delete_png_file(image)
        delete_google_drive_file(file_id)



#The master function where everything comes together. The screenshots are taken, the images are 
#cropped, the images are put into google drive, then found and replaced in the reports, then the
#image files are deleted, and then the google drive files are deleted.
def master():
    images = take_screenshots_and_crop_images()
    find_and_replace_ahrefs_images_into_reports(images)


master()