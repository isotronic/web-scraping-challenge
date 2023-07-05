from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfzkv9bvaDEVAzFlyeVGQ9s-6fGy1YJJpNHpExAPenu9qtHqg/viewform?usp=sf_link"
DATA_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.53615416479492%2C%22east%22%3A-122.33531035375977%2C%22south%22%3A37.70945520980244%2C%22north%22%3A37.81720606103099%7D%2C%22mapZoom%22%3A13%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A391526%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A2000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

# Chrome options for Selenium
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Chrome WebDriver service
service = Service(r"C:\Users\infam\OneDrive\Desktop\dev\chromedriver.exe")


# Function to retrieve web page content and store it in a file
def get_web_page(file, url):
    try:
        open(file)
    except FileNotFoundError:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)

        go = input("Allow the page to completely render and type 'y' to save to file: ")
        if go == "y":
            html_source = driver.page_source
            with open(file=file, mode="w", encoding="utf-8") as fp:
                fp.write(html_source)
        driver.quit()
    else:
        pass
    finally:
        with open(file=file, mode="r", encoding="utf-8") as fp:
            content = fp.read()
        return BeautifulSoup(content, "html.parser")


# Get web page content using BeautifulSoup
soup = get_web_page(file="web_page.html", url=DATA_URL)

# Extract property links and addresses from the web page
link_tags = soup.select('a[data-test="property-card-link"]')
links = [link.get("href") for link in link_tags if link.get("tabindex") == "0"]
for index in range(len(links)):
    if not links[index].startswith("http"):
        links[index] = "https://www.zillow.com" + links[index]

addresses = [link.text for link in link_tags if link.get("tabindex") == "0"]

# Extract property prices from the web page
price_tags = soup.select('span[data-test="property-card-price"]')
prices = [price.text.split("/")[0].split("+")[0] for price in price_tags]

# Open the Google Form in Chrome using Selenium WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(FORM_URL)

# Fill in the form with property details
for n in range(len(links)):
    time.sleep(2)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses[n])

    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(prices[n])

    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(links[n])

    send_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    send_btn.click()

    time.sleep(1)
    continue_link = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    continue_link.click()

driver.quit()

