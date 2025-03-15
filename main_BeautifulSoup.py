from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

# Setup Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--incognito")  # Open browser in incognito mode
# options.add_argument("--headless=new")  # Use only if you don't need to see the browser

# Initialize WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Open Amazon's mobile phone search results page (Modify the price range as needed)
amazon_url = "https://www.amazon.in/s?k=mobile+phones&rh=p_36%3A1000000-2000000"
driver.get(amazon_url)

# Random delay to mimic human behavior
time.sleep(random.uniform(5, 9))

# Get the full page source
html = driver.page_source
driver.quit()  # Close Selenium

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Find all product containers
phones = soup.find_all("div", {"data-component-type": "s-search-result"})

print(f"Found {len(phones)} mobile phones:")

# List to store extracted data
data = []

# Extract product details
for phone in phones:
    try:
        # ✅ Extract Title
        title_element = phone.find("h2")
        title = title_element.text.strip() if title_element else "N/A"

        # ✅ Extract Phone Link
        link_element = phone.find("a") if title_element else None
        phone_link = "https://www.amazon.in" + link_element["href"] if link_element else "N/A"

        # ✅ Extract Price (only 'a-price-whole' since no fractions exist)
        price_element = phone.find("span", class_="a-price-whole")
        price = price_element.text.strip() if price_element else "N/A"

        print(f"Title: {title}")
        print(f"Price: ₹{price}")
        print(f"Link: {phone_link}")
        print("-" * 50)

        # Append data to list
        data.append({"Phone Name": title, "Price": price, "Link": phone_link})          

    except Exception as e:
        print("Error extracting details:", e)

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv("amazon_mobiles_BeautifulSoup.csv", index=False, encoding="utf-8-sig")

print("\n✅ Data saved successfully to 'amazon_mobiles.csv'")