import initialize_apis
from initialize_apis import get_slides_and_drive_apis
import os
from selenium import webdriver
from PIL import Image
from io import BytesIO
import googleslidesproject
from googleslidesproject import find_replace_img
from apiclient.http import MediaFileUpload

port = 5005
urls = ['/content_report_month', '/content_next_month']
#url = 'http://127.0.0.1:' + str(port) + '/content_report_month'
pres_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
#shape_text = '{{content_report_month}}'
slides_service = get_slides_and_drive_apis.setup_googleslides_api()
drive_service =  get_slides_and_drive_apis.initialize_drive()
folder_id = '1hScQyb1uMLQaBmNgyHa1dlFZAO2mKzxC'
page_id = 'g202ad04c01_0_6'


def take_ss(url):
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    image_url = 'content_screenshot.png'
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

def get_file_id(image_url):
    file_metadata = {'name': image_url,
    'parents': [folder_id]}
    media = MediaFileUpload(image_url, mimetype='image/jpeg', resumable = True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    return file_id

def get_new_image_url(file_id):
    new_image_url = 'https://drive.google.com/uc?id=' + file_id
    return new_image_url



def delete_png_file(image_url):
    os.remove(image_url)



def delete_google_drive_file(file_id):
    service = drive_service
    file_metadata = {'trashed':True}
    file = drive_service.files().update(body=file_metadata, fileId = file_id).execute()






def master(urls):
    for url in urls:
        url = 'http://127.0.0.1:' + str(port) + url
        image_url = take_ss(url)
        file_id = get_file_id(image_url)
        new_image_url = get_new_image_url(file_id)
        if 'report' in url:
            shape_text = 'content_report_month'
            find_replace_img(pres_id, shape_text, new_image_url)
        else:
            shape_text = 'content_next_month'
            find_replace_img(pres_id, shape_text, new_image_url)
        delete_png_file(image_url)
        delete_google_drive_file(file_id)

master(urls)