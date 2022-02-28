#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from bs4 import BeautifulSoup
from six.moves.urllib.request import urlopen as ur
import codecs
#import six
#from io import open
from requests import get
import json
import re
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

def insert_pipe(string, index):
    return string[:index] + '|' + string[index:]
    
for i in range(1,3847):
  print(i)
  url = 'https://nabory.kprm.gov.pl/wyniki-naborow?AdResult%5BpagesCnt%5D=10&AdResult%5BisAdvancedMode%5D=&AdResult'\
  '%5Bsort%5D=1&AdResult%5Bid%5D=&AdResult%5Bid_institution%5D=&AdResult%5Bid_institution_position%5D=&search-button='\
  + '&page=' + str(i) + '&per-page=20'
  # zapisuje adres url do zmiennej i pobieram tresc strony
  page = get(url)
  bs = BeautifulSoup(page.content, 'html.parser')
  for element in bs.find_all('li', class_= 'row'):
    # pobieram podstawowe dane o kazdym naborze ze strony glownej
    job_id = element.find('span', class_='id').get_text()
    job_title = element.find('strong', class_='title').get_text()
    institution = element.select('div > b')[0].get_text(strip=True)
    city = element.select('div > b')[1].get_text(strip=True)
    announcement_date = element.select('div > b')[2].get_text(strip=True)

    # pobieram odnosnik ze strony glownej do podstrony kazdego wyniku, chce pobrac wynik naboru
    link = element.find('a', class_='single').get('href')
    url2 = "https://nabory.kprm.gov.pl" + link
    
    
    bs2 = BeautifulSoup(get(url2).content, 'html.parser')
    result1 = bs2.find('div', class_='row job-res').get_text().strip()
    result2 = re.sub(r'(\s+|\n)', ' ', result1)
    
    if ('anulowano nabór') in result2:
      index = result2.find('nabór') + len('nabór')
      result2 = insert_pipe(result2, index)
    elif ('nabór zakończony wyborem kandydatki/kandydata') in result2:
      index = result2.find('kandydata') + len('kandydata')
      result2 = insert_pipe(result2, index)
    result_date = bs2.select('li > div')[1].get_text().strip()
    
    # pobieram odnosnik do strony z ogloszeniem w celu uzyskania opisu stanowiska, pensji itd.
    link2 = bs2.find('a', class_='btn btn-b').get('href')
    url3 = 'https://nabory.kprm.gov.pl' + link2
    url3 = url3.replace(",v7", "")
    
    bs3 = BeautifulSoup(get(url3).content, 'html.parser')
    if bs3.find('div', class_ = 'info-circle__content info-circle__content--salary info-circle__content--small-text'):
      salary = \
      bs3.find('div', class_ = 'info-circle__content info-circle__content--salary info-circle__content--small-text').get_text().strip()
    else:
      salary = 'nie podano wynagrodzenia'
    if bs3.find('div', class_= 'box cir cir-1 cir-status')  :
      state = bs3.find('div', class_= 'box cir cir-1 cir-status').get_text().strip()
    else:
      state = 'brak danych'
    
    work_time = bs3.find('div', class_ = 'box cir cir-').get_text().strip()
    positions = bs3.find('div', class_ = 'box cir cir-').findNext('div').get_text().strip()
    
    if bs3.find('div', class_ = 'ar'):
      responsibilities = bs3.select('div > section')[1].findChildren('li')
      for index, item in enumerate(responsibilities):
        responsibilities[index] = item.get_text()
#       else:
#         responsibilities = 'nie podano zadań'
      
      requirements = bs3.select('div > section')[2].findChildren('li')
      education = requirements[0].get_text()
      requirements.pop(0)
      for id, requirement in enumerate(requirements):
        requirements[id] = re.sub(r'(\s+|\n)', ' ', requirement.get_text())
#       else:
#         requirements = 'brak wymagan'
      
      additional_requirements = bs3.select('div > section')[3].findChildren('li')
      for ind, additional in enumerate(additional_requirements):
        additional_requirements[ind] = re.sub(r'(\s+|\n)', ' ', additional.get_text())
#       else:
#         additional_requirements = 'brak dodatkowych wymagan'
      
    if bs3.find('div', class_ = 'col-lg-12'):
      views = bs3.find('div', class_ = 'col-lg-12').get_text()
    else:
      views = 'brak liczby odwiedzin'
      # dane do pliku json o nazwie 'data'
    data = [job_id, job_title, institution, city, announcement_date,re.sub(r'(\s+|\n)', ' ', result_date),
    re.sub(r'(\s+|\n)', ' ', result2), re.sub(r'(\s+|\n)', ' ', salary), positions,
    work_time, state, responsibilities,
    re.sub(r'(\s+|\n)', ' ', education), requirements,
    additional_requirements, re.sub(r'(\s+|\n)', ' ', views)]
      
    with codecs.open('kprm-old-data.json', 'a') as f:
      json.dump(data, f, ensure_ascii=False)
      f.write('\n')
