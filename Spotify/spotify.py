from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


url = r"https://open.spotify.com/artist/2PgD2yAtkUcDgZ1Yz0SPSA#_=_"

driver = webdriver.Chrome('/Users/gz5710/Downloads/chromedriver')
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
print(soup)

driver.quit()