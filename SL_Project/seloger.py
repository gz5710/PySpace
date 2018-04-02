from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import logging
from logging.handlers import RotatingFileHandler
from mysql_helper import MysqlHelper

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



curr_page = 1
url_base = r"http://www.seloger.com/list.htm?types=1&projects=2&natures=1,2,4&places=[{ci:780646}]&qsVersion=1.0&engine-version=new&LISTING-LISTpg="
url = f"{url_base}{curr_page}"
# url = r'http://www.seloger.com/list.htm?types=1&projects=2,5&natures=1,2,4&price=NaN/270000&surface=50/NaN&rooms=2,3&places=[{ci:780646}|{ci:780686}]&qsVersion=1.0&engine-version=new'
# url = r'http://www.seloger.com/list.htm?types=1&projects=2,5&natures=1,2,4&price=NaN/270000&surface=50/NaN&rooms=2,3&places=[{ci:780646}|{ci:780686}]&qsVersion=1.0&engine-version=new&LISTING-LISTpg=2'

driver = webdriver.Chrome('/Users/gz5710/Downloads/chromedriver')
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')


try:    
    total_anno_nb = int(soup.select('div.title_nbresult')[0].text.split(' ')[0])
    total_page_nb = int(total_anno_nb / 20) + 1
    logger.debug(f"We got {total_anno_nb} annonces on {total_page_nb} pages")
    if total_anno_nb == 0:
        exit()
except Exception as ex:
    logger.error(f"Error in getting number of annonces\n{ex}")
    exit()

while curr_page <= total_page_nb:
    try:    
        annonces = {}
        lists = soup.select('div.c-pa-list')
        for a in lists:
            # Parse html to dict
            anno = {}  
            anno['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            anno['id'] = a['id']
            anno['title'] = a.select('a.c-pa-link')[0]['title'].strip()
            anno['link'] = a.select('a.c-pa-link')[0]['href']
            for em in a.select('div.c-pa-criterion em'):
                if 'p' in em.text:
                    anno['piece'] = em.text.split(' ')[0]
                elif 'ch' in em.text:
                    anno['room'] = em.text.split(' ')[0]
                elif 'm²' in em.text:
                    anno['surface'] = em.text.split(' ')[0].replace(',', '.')
            anno['price'] = a.find('span', {'class':'c-pa-cprice'}).text.replace('\n', '').replace(' ', '').replace('\xa0', '').replace('\u20ac', '')
            anno['currency'] = 'EUR'
            anno['price_updated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            anno['city'] = a.select('div.c-pa-city')[0].text
            if a.select('div.c-pa-agency a') != []:
                anno['agency_link'] = a.select('div.c-pa-agency a')[-1]['href']
            if a.select('div.c-pa-actions a[tabindex=0]') != []:
                anno['agency_tel'] = a.select('div.c-pa-actions a[tabindex=0]')[0]['data-tooltip-focus']
            anno['available'] = True
            anno['source'] = 'seloger'
            anno['type'] = 1
            
            annonces[anno['id']] = anno
        
        # MysqlHelper.InsertDictAnnonces(annonces)

        # save result to JSON
        json = json.dumps(annonces)
        f = open(f"{os.path.dirname(__file__)}/records/sl-{datetime.now().strftime('%Y-%m-%d')}.json","a+")
        f.write(json)
        f.close()
    except Exception as ex:
        logger.error(f"Error happens on the page {url}\n{ex}")
    finally:
        # find next page
        curr_page += 1
        url = f"{url_base}{curr_page}"
        if curr_page <= total_page_nb:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.close()