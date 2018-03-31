from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import logging
from logging.handlers import RotatingFileHandler

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
 
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler(f"{os.path.dirname(__file__)}/logs/sl_log-{datetime.now().strftime('%Y-%m-%d')}.log", 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# url = r'http://www.seloger.com/list.htm?types=1&projects=2,5&natures=1,2,4&price=NaN/270000&surface=50/NaN&rooms=2,3&places=[{ci:780646}|{ci:780686}]&qsVersion=1.0&engine-version=new'
# url = r'http://www.seloger.com/list.htm?types=1&projects=2,5&natures=1,2,4&price=NaN/270000&surface=50/NaN&rooms=2,3&places=[{ci:780646}|{ci:780686}]&qsVersion=1.0&engine-version=new&LISTING-LISTpg=2'
url = r'http://www.seloger.com/list.htm?tri=initial&idtypebien=1&idtt=2,5&naturebien=1,2,4&ci=780646'

driver = webdriver.Chrome('/Users/gz5710/Downloads/chromedriver')
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

annonces = {}

try:    
    total_anno_nb = int(soup.select('div.title_nbresult')[0].text.split(' ')[0])
    total_page_nb = int(total_anno_nb / 20) + 1
    logger.debug(f"We got {total_anno_nb} annonces on {total_page_nb} pages")
    if total_anno_nb == 0:
        exit()
except Exception as ex:
    logger.error(f"Error in getting number of annonces\n{ex}")

curr_page = 1
url_base = r"http://www.seloger.com/list.htm?types=1&projects=2&natures=1,2,4&places=[{ci:780646}]&qsVersion=1.0&engine-version=new&LISTING-LISTpg="
while curr_page <= total_page_nb:
    try:    
        # print(soup.prettify())
        lists = soup.select('div.c-pa-list')
        for a in lists:
            anno = {}  
            # print('====================================================')
            # print(t['title'])
            anno['id'] = a['id']
            # print(anno['id'])
            anno['title'] = a.select('a.c-pa-link')[0]['title'].strip()
            # print(anno['title'])
            anno['link'] = a.select('a.c-pa-link')[0]['href']
            # print(anno['link'])
            anno['criterion'] = f"{a.select('div.c-pa-criterion em')[0].text} / {a.select('div.c-pa-criterion em')[1].text} / {a.select('div.c-pa-criterion em')[2].text}"
            # print(anno['criterion'])
            anno['price'] = a.find('span', {'class':'c-pa-cprice'}).text.replace('\n', '').replace(' ', '').replace('\xa0', ' ')
            # print(anno['price'])
            anno['city'] = a.select('div.c-pa-city')[0].text
            # print(anno['city'])
            if a.select('div.c-pa-agency a') != []:
                anno['agency'] = a.select('div.c-pa-agency a')[-1]['href']
            else:
                anno['agency'] = None
            
            # print(anno['agency'])
            if a.select('div.c-pa-actions a[tabindex=0]') != []:
                anno['tel'] = a.select('div.c-pa-actions a[tabindex=0]')[0]['data-tooltip-focus']
            else:
                anno['tel'] = None
            
            # print(anno['tel'])
            # print(anno)
            # print('====================================================')
            annonces[anno['id']] = anno
        
        # print(annonces)
        # save result to JSON
        json = json.dumps(annonces)
        f = open(f"{os.path.dirname(__file__)}/records/sl-{datetime.now().strftime('%Y-%m-%d')}.json","a+")
        f.write(json)
        f.close()

        
        
    except Exception as ex:
        print(ex)
    finally:
        # find next page
        curr_page += 1
        url = f"{url_base}{curr_page}"
        if curr_page <= total_page_nb:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.close()