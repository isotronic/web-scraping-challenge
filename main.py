from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfzkv9bvaDEVAzFlyeVGQ9s-6fGy1YJJpNHpExAPenu9qtHqg/viewform?usp=sf_link"
DATA_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.53615416479492%2C%22east%22%3A-122.33531035375977%2C%22south%22%3A37.70945520980244%2C%22north%22%3A37.81720606103099%7D%2C%22mapZoom%22%3A13%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A391526%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A2000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.9,de;q=0.8,en-US;q=0.7",
}

# fetch the website and collect links, addresses and prices for each listing in separate lists
response = requests.get(DATA_URL, headers=headers)
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")

link_tags = soup.select('a[data-test="property-card-link"]')
links = [link.get("href") for link in link_tags if link.get("tabindex") == "0"]

addresses = [link.text for link in link_tags if link.get("tabindex") == "0"]

price_tags = soup.select('span[data-test="property-card-price"]')
prices = [price.text.split("/")[0].split("+")[0] for price in price_tags]

# open the form and type in the data for each item in the previously collected lists
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = Service(r"C:\Users\infam\OneDrive\Desktop\dev\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(FORM_URL)

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

