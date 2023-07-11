# BA024webscraping_taobao.com
This project is a special one among projects.
First, it requires customer verification to get access to the website.
Second, the website has varied customer review links which are all json format Ajax link.
To address the obstacles.

1. this code uses selenium to get logging information and access to the target website.
2. the code will utilize selenium to open each of product links and depend on a series of manipulation to load customer reivews.
3. all the reviews will be loaded in a response and pass to scrapy to decode.
