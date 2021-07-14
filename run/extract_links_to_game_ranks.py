from selenium import webdriver
from bs4 import BeautifulSoup

driver_path = '../resources/chromedriver' # driver path
url = 'https://play.google.com/store/apps/top/category/GAME'

browser = webdriver.Chrome(executable_path=driver_path) # Chrome driver
browser.get(url)

page = browser.page_source
soup = BeautifulSoup(page, "html.parser")
links = soup.find_all('div', {'class': 'W9yFB'}) # find all links to rankings

for link in links:
    new_url = link.a['href']
    print(new_url)
    browser.get("https://play.google.com"+new_url)

browser.quit()