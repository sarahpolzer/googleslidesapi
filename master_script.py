#from initialize_apis import get_slides_and_drive_apis
#slides_service = get_slides_and_drive_apis.setup_googleslides_api()
#drive_service =  get_slides_and_drive_apis.initialize_drive()
#import google_slides_functions 
#import master_script 
#import  master_screenshots 
#import extraneous_find_and_replace
#from ahrefs_scrape import take_ahrefs_screenshots
import json 
    

with open('client_information/client_information.json', 'r') as f:
     clients = json.load(f)
client = input('Who is the client? ')

import flask_screenshots
import ahrefs_scrape
import extraneous_find_and_replace


