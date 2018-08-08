from __main__ import *

#A function to take screenshots of domains and keywords charts from ahrefs and place them into reports
def ahrefs_scrape_master(clients, client, domains_image, keywords_image, images, ahrefs_un, ahrefs_pw, folder_id, drive_service):
    pres_id = clients[client]['presentation_id']
    referring_domains = '{{domains}}' #string to find and replace with ahrefs data in report
    referring_pages = '{{pages}}' #string to find and replace with ahrefs data in report
    org_keywords = '{{org_keywords}}'#string to find and replace with ahrefs data in report
    traffic_value = '{{traffic_value}}'
    new_keywords = '{{new_keywords}}'
    def take_ahrefs_screenshots():
        domain_name = clients[client]['domain_name'].replace("https://", "").replace("http://", "").replace('www/', 'www.')
        chromedriver = "/usr/local/bin/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        driver.implicitly_wait(10) # seconds
        driver.get("https://ahrefs.com/user/login/")
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
        #This is a little confusing. I am automatically placing the number of referring domains on
        #the ahrefs page into the report over the string {{domains}}
        r_domains = driver.find_element_by_xpath('//td[@class="text-xs-right highlight-link"][1]').text
        find_replace_str(pres_id, referring_domains, r_domains )
        #I am automatically placing the number of referring pages from the ahrefs page into the
        #report over the string {{pages}}
        r_pages = driver.find_element_by_xpath('//span[@id="ref_pages_val"]/a').text
        find_replace_str(pres_id, referring_pages, r_pages)
        #I am automatically placing the traffic value from the ahrefs page into the report
        #over the string {{traffic_value}}
        t_value = driver.find_element_by_xpath('//h5[@id="numberOfOrganicTrafficCost"]/span').text
        find_replace_str(pres_id, traffic_value, t_value)
        driver.find_element_by_xpath('//li[@name="se-overview-tabs"][2]/a').click()
        sleep(15)
        driver.implicitly_wait(10) # seconds
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 8);")
        driver.save_screenshot(keywords_image)
        #I am automatically placing the number of organic keywords from the ahrefs page into 
        #the report over the string {{org_keywords}}
        o_keywords = driver.find_element_by_xpath('//span[@id="organic_keywords_val"]').text
        find_replace_str(pres_id, org_keywords, o_keywords )
        driver.get('https://ahrefs.com/positions-explorer/new-keywords/v2/subdomains/us/2018-08-08/all/all/1/volume_desc?target=' + domain_name + '%2F')
        try:
            n_keywords = driver.find_element_by_xpath('//div[@name="result_info"]/var').text
            find_replace_str(pres_id, new_keywords, n_keywords)
        except:
            pass
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