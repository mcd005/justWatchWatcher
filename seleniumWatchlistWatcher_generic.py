from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--start-maximized")
options.add_argument('''<This is where you cna include the path to your Chrome profile. Makes logging into JW easier since the it's linked to my Chrome account>''')

#So Selenioum knows where to launch chrome from
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)

#Open page
driver.get('https://www.justwatch.com/uk')

#These are included throughout so a page has enough time to render before the next action is taken
#There is probably a more sophisticated way of doing this (e.g. asking Selenium to check if the page is done) loading, but this works well for now
time.sleep(3)

#The following section was for navigating through various login pages but was made obselte after I linked my chrome account
#Navigation was done through identifying CSS/XML paths or HTML ids. Honestly it's a little labourious.
'''
#Allow some time to load
time.sleep(3)

sign_in_btn = driver.find_element_by_xpath('//ion-button[@class="basic-button rounded ion-color ion-color-tertiary md button button-default button-solid ion-activatable ion-focusable hydrated"]')
sign_in_btn.click()

time.sleep(1)

sign_in_btn2 = driver.find_element_by_xpath('//button[@class="account-modal-button mb"]')
sign_in_btn2.click()

time.sleep(1)

google_btn = driver.find_element_by_xpath('(//div[@class="button"])[3]')
google_btn.click()

driver.switch_to.window(driver.window_handles[1])

time.sleep(1)

google_user = driver.find_element_by_id('identifierId')
google_user.send_keys(<YOUR EMAIL>)
google_user.send_keys(Keys.RETURN)

time.sleep(1)

google_pass = driver.find_element_by_xpath('//input[@class="whsOnd zHQkBf"]')
google_pass.send_keys(<YOUR PASSWORD>)
google_pass.send_keys(Keys.RETURN)
'''

driver.quit()

# #Looks through the page to find all elements that match this ID/class name
# titles = driver.find_elements_by_xpath('//div[@class="title-list-grid__item"]')
#
# #Iterates through the items and extracts the tidy titles from the HTML
# for title in titles:
#     title_html = title.get_attribute('innerHTML')
#     result = re.search('alt="(.*)" class', title_html)
#     print(result.group(1))

