from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless=new")  # for Chrome >= 109

driver = webdriver.Chrome(options=chrome_options)

from scraping import MenyScraper

scraper = MenyScraper(driver)

rootPage = 'https://meny.no/varer/middag/ris'
scraper.scrape(rootPage)


driver.close()