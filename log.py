"""
# Project: Simulate logging
# Author: Eddie
# Date: 07/07/2023
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait
import json
from utils import create_chrome_driver

browser = create_chrome_driver()
browser.get('https://login.taobao.com')

browser.implicitly_wait(10)

username_input = browser.find_element(By.CSS_SELECTOR, '#fm-login-id')
username_input.send_keys('17547968757')
username_input = browser.find_element(By.CSS_SELECTOR, '#fm-login-password')
username_input.send_keys('qwer1122')
login_button = browser.find_element(By.CSS_SELECTOR, '#login-form > div.fm-btn > button')
login_button.click()

time.sleep(10)
wait_obj = WebDriverWait(browser, 10)
wait_obj.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m-userinfo')))

with open('taobao.json', 'w') as file:
    json.dump(browser.get_cookies(), file)