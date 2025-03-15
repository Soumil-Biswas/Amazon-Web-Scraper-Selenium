# Amazon-Web-Scraper-Selenium
 An web scraping bot for retrieving mobile phone prices. Built using Python, selenium and BeautifulSoup

# Dependencies
 The following python dependencies need to be installed before this script can be run:

 1. selenium
 2. bs4
 3. pandas

# How to run
 Run any one among `main_Selenium.py` , `main_BeutifulSoup.py` , `main_Selenium_Stage_2.py` in a python IDE of your choice.

 `main_Selenium.py` scrapes a single page using Selenium and saves the records in `amazon_mobiles_Selenium.csv`. The search Query and price range is hardcoded into the amazon.in search URL.

 `main_BeutifulSoup.py` scrapes a single page using Selenium, parses the information using BeautifulSoup (bs4) and saves the records in `amazon_mobiles_BeutifulSoup.csv`. The search Query and price range is hardcoded into the amazon.in search URL.

 `main_Selenium_Stage_2.py` scrapes 20 pages using Selenium and BeutifulSoup saves the records in `amazon_mobiles_Selenium_Stage_2.csv`. The bot manually searches for mobile phones using Amazon's search bar and sets the price range in Amazon's price range slider.

 ![Screenshot 2025-03-15 110959](https://github.com/user-attachments/assets/b46b6814-2fa1-42bf-acb4-a75ca645f49f)

 ![Screenshot 2025-03-15 111016](https://github.com/user-attachments/assets/00f109cc-af16-45f9-91e3-05c662f3b84d)
