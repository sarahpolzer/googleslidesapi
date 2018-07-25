import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

#don't forget to add your environmental variables
ahrefs_pw = os.environ['AHREFS_PW']
ahrefs_un = os.environ['AHREFS_UN']
domain_name = 'kppblaw.com'
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
#driver = webdriver.Firefox()

def take_ahrefs_screenshots():
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
    driver.save_screenshot('domains_count.png')
    driver.find_element_by_xpath('//li[@name="se-overview-tabs"][2]/a').click()
    sleep(15)
    driver.implicitly_wait(10) # seconds
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 6);")
    driver.save_screenshot('keyword_count.png')
    driver.close()
    

take_ahrefs_screenshots()


