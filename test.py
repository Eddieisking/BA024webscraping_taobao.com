"""
# Project:
# Author: Eddie
# Date: 
"""
import time

from utils import create_chrome_driver, add_cookies

browser = create_chrome_driver()
browser.get('https://taobao.com')
add_cookies(browser, 'taobao.json')
browser.get('https://s.taobao.com/search?q=%E5%BE%97%E4%BC%9F%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%E5%AE%98%E7%BD%91&s=0')
time.sleep(10)