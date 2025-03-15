from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
time.sleep(random.uniform(3, 7))

# Extract mobile phone details
phones = driver.find_elements(By.XPATH, "//div[contains(@class, 's-main-slot')]//div[@data-component-type='s-search-result']")

print(f"Found {len(phones)} mobile phones:")

# List to store extracted data
data = []

for phone in phones:
    try:
        # Extract phone title
        title_element = phone.find_element(By.XPATH, ".//a/h2")
        title = title_element.text
        link = title_element.get_attribute("href")

        # Extract price (if available)
        try:
            price_whole = phone.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            # price_fraction = phone.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
            # price = f"₹{price_whole}.{price_fraction}"
            price = f"₹{price_whole}"
        except:
            price = "Price not available"

        print(f"📱 {title} - {price}")
        print(f"🔗 {link}\n")

        # Append data to list
        data.append({"Phone Name": title, "Price": price, "Link": link})        

    except Exception as e:
        print(f"Error extracting phone details: {e}")

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv("amazon_mobiles_Selenium.csv", index=False, encoding="utf-8-sig")

print("\n✅ Data saved successfully to 'amazon_mobiles.csv'")

# Close the browser after scraping
time.sleep(random.uniform(3, 5))
driver.quit()