import initialize_apis
from initialize_apis import get_slides_and_drive_apis
import os
from selenium import webdriver
from PIL import Image
from io import BytesIO
import googleslidesproject
from googleslidesproject import find_replace_img
from apiclient.http import MediaFileUpload

port = 5004
url = 'http://127.0.0.1:' + str(port) + '/traffic'
pres_id = '17qSfATi1I-0HmQ7LoEgCrz-DkOdw7qt1p4ATg9oika8'
shape_text = '{{traffic}}'
slides_service = get_slides_and_drive_apis.setup_googleslides_api()
drive_service =  get_slides_and_drive_apis.setup_googledrive_api()


def take_ss(url):
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    image_url = 'traffic_screenshot.png'
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
    file_metadata = {'name': image_url}
    media = MediaFileUpload(image_url, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def master(url):
    image_url = take_ss(url)
    get_file_id(image_url)




master(url)