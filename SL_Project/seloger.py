from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

url = r'http://www.seloger.com/list.htm?types=1&projects=2,5&natures=1,2,4&price=NaN/270000&surface=50/NaN&rooms=2,3&places=[{ci:780646}|{ci:780686}]&qsVersion=1.0&engine-version=new'
# url = r'http://www.seloger.com/list.htm?types=1&projects=2,5&natures=1,2,4&price=NaN/270000&surface=50/NaN&rooms=2,3&places=[{ci:780646}|{ci:780686}]&qsVersion=1.0&engine-version=new&LISTING-LISTpg=2'

driver = webdriver.Chrome('/Users/gz5710/Downloads/chromedriver')
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

annonces = {}

try:    
    # print(soup.prettify())
    lists = soup.select('div.c-pa-list')
    i = 0
    for a in lists:
        anno = {}  
        print('====================================================')
        # print(t['title'])
        i += 1
        anno['index'] = i
        anno['id'] = a['id']
        print(anno['id'])
        anno['title'] = a.select('a.c-pa-link')[0]['title'].strip()
        print(anno['title'])
        anno['link'] = a.select('a.c-pa-link')[0]['href']
        print(anno['link'])
        anno['criterion'] = f"{a.select('div.c-pa-criterion em')[0].text} / {a.select('div.c-pa-criterion em')[1].text} / {a.select('div.c-pa-criterion em')[2].text}"
        print(anno['criterion'])
        anno['price'] = a.find('span', {'class':'c-pa-cprice'}).text.replace('\n', '').replace(' ', '').replace('\xa0', ' ')
        print(anno['price'])
        anno['city'] = a.select('div.c-pa-city')[0].text
        print(anno['city'])
        if a.select('div.c-pa-agency a') != []:
            anno['agency'] = a.select('div.c-pa-agency a')[-1]['href']
        else:
            anno['agency'] = 'null'
        
        print(anno['agency'])
        if a.select('div.c-pa-actions a[tabindex=0]') != []:
            anno['tel'] = a.select('div.c-pa-actions a[tabindex=0]')[0]['data-tooltip-focus']
        else:
            anno['tel'] = 'null'
        
        print(anno['tel'])
        # print(anno)
        print('====================================================')
        annonces[anno['id']] = anno
    
    print(annonces)
    # save result to JSON
    json = json.dumps(annonces)
    f = open(f"{os.path.dirname(__file__)}/records/sl-{datetime.now().strftime('%Y-%m-%d')}.json","a+")
    f.write(json)
    f.close()
    
except Exception as ex:
    print(ex)
finally:
    driver.close()