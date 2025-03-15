from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Open Amazon's Page
amazon_url = "https://www.amazon.in"
driver.get(amazon_url)
time.sleep(3)  # Let the page load

# Locate the search bar and enter the query
search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys("mobile phones")  # Enter search term
search_box.send_keys(Keys.RETURN)  # Press Enter
time.sleep(3)  # Wait for results to load

# Apply price filter
min_price = "10000"
max_price = "20000"

# Find the min price and max price input boxes
try:
    driver.execute_script("""
        document.getElementsByName('low-price')[0].value = arguments[0];
        document.getElementsByName('high-price')[0].value = arguments[1];
    """, min_price, max_price)
    print("price modified")

    time.sleep(1)  # Let values update
    go_button = driver.find_element(By.XPATH, "//input[@aria-label='Go - Submit price range']")

    go_button.click()
    time.sleep(3)  # Wait for page refresh
except:
    print("Price filter inputs not found, continuing without it.")

# List to store extracted data
data = []

# Extract product details
def extract_data(url):

    # Random delay to mimic human behavior
    time.sleep(random.uniform(2, 3))

    # Get the full page source
    html = url

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all product containers
    phones = soup.find_all("div", {"data-component-type": "s-search-result"})

    print(f"Found {len(phones)} mobile phones:")

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

            # print(f"Title: {title}")
            # print(f"Price: ₹{price}")
            # print(f"Link: {phone_link}")
            # print("-" * 50)

            # Append data to list
            data.append({"Phone Name": title, "Price": price, "Link": phone_link})          

        except Exception as e:
            print("Error extracting details:", e)

    return soup  # Return soup to find next page

page_number = 1
current_url = driver.page_source

# 🔹 Step 4: Loop Through Multiple Pages
while True:

    print(f"\nScraping Page {page_number}...")
    soup = extract_data(current_url)    # Scrape current page

    try:
        # Locate the "Next" button
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")

        # Check if "Next" button is disabled (last page)
        if "s-pagination-disabled" in next_button.get_attribute("class"):
            print("✅ No more pages to scrape. Exiting loop.")
            break

        # Click the next page button
        print("➡️ Moving to the next page...")
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)  # Wait for page load

        page_number += 1

    except Exception:
        print("No 'Next' button found. Ending scrape.")
        break  # Exit loop if no "Next" button

driver.quit()  # Close Selenium      

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv("amazon_mobiles_Selenium_Stage_2.csv", index=False, encoding="utf-8-sig")

print("\n✅ Data saved successfully to 'amazon_mobiles_Selenium_Stage_2.csv'")