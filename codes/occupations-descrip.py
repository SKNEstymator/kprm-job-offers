from bs4 import BeautifulSoup
from requests import get
import re
import json

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Ł',
           'M', 'N', 'O', 'P', 'R', 'S', 'Ś', 'T', 'U', 'W', 'Z', 'Ż']
for i in letters:
  print(i)
  url = 'https://psz.praca.gov.pl/rynek-pracy/bazy-danych/'\
  'klasyfikacja-zawodow-i-specjalnosci/wyszukiwarka-opisow-zawodow'\
  '//-/klasyfikacja_zawodow/litera/' + str(i)
  page = get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  for element in soup.find_all('tr', class_ = ''):
    id = element.find('td', class_ = 'first').get_text()
    title = element.find('a', class_ = 'viewMore').get_text().strip()
    url_2 = element.find('a', class_ = 'viewMore').get('href')
    soup_2 = BeautifulSoup(get(url_2).content, 'html.parser')
    synthesis = soup_2.find_all('td')[3].get_text().strip()
    tasks = soup_2.find_all('td')[4].get_text().strip()
    data = [id, re.sub(r'(\s+|\n)', ' ', title), re.sub(r'(\s+|\n)', ' ', synthesis), re.sub(r'(\s+|\n)', ' ', tasks)]
    with open('occup-desc.json', 'a', encoding='utf-8') as f:
      f.writelines(str(data)+'\n')
