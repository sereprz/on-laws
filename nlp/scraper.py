import re
import time
import json
from selenium import webdriver
from collections import defaultdict

from bs4.element import Tag
from bs4 import BeautifulSoup


BASEURL = 'https://www.ontario.ca'

def get_first(soup):
    '''
        get the first law-level element
    '''
    levels = soup.find_all(attrs={'class': re.compile('law-level-[123]')})
    
    return [el for el in levels if isinstance(el, Tag) and isinstance(el.parent, Tag) and el.parent.name != 'td'][0]


def update_levels(el, level1, level2, level3):
    '''
        :param el: html element
        :param level1: string, Part number e.g. Part III Accessibility Standards
        :param level2: string, Heading e.g. Establishment Of Standards
        :param level3: string, Headnote e.g. Accessibility standards established by regulation
        
    '''

    text = re.sub('\xa0|\r\n|\s{2,}', ' ', el.text.strip())

    if 'law-level-1' in el.attrs['class']:
        return (text, level2, level3)
    
    if 'law-level-2' in el.attrs['class']:
        return (level1, text, level3)    
    
    if 'law-level-3' in el.attrs['class']:
        return (level1, level2, text)


def get_content(soup):

    content = []
    
    try:
        first = get_first(soup)
        counter = 0
    except IndexError:
        return content

    level1, level2, level3 = update_levels(first, '', '', '')
    
    for el in first.find_all_next():
        
        if isinstance(el, Tag):
            
            try:
                class_ =  '.'.join(el.attrs['class'])
            except KeyError:
                class_ = ''
            
            if 'line' in class_:
                return content
            
            if 'law-level' in class_ and 'headnoteChar' not in class_:
                level1, level2, level3 = update_levels(el, level1, level2, level3)
            else:
                if el.name == 'p' and class_ != 'table':
                    counter += 1
                    content.append(
                        {'id': counter,
                         'level1': level1,
                         'level2': level2,
                         'level3': level3,
                         'name': el.name,
                         'text': re.sub(r'\xa0|\r\n', ' ', el.text.strip()),
                         'class': el.attrs['class'] if 'class' in el.attrs else '',
                        }
                    )
    return content

print(f'Scraping {BASEURL}"/laws"..')
start = time.time()

next_page = '/laws'

statutes = []
driver = webdriver.Firefox(executable_path='geckodriver/geckodriver')

while next_page:
    print(f'Scraping law titles/urls from {BASEURL}{next_page}...')
    driver.get(f'{BASEURL}{next_page}')
    soup = BeautifulSoup(driver.page_source, 'lxml')

    records = soup.find_all('td')
    
    for r in records:
    
        a = r.find_next('a')
        statutes.append({
            'act': a.text.strip(),
            'url': a.attrs['href']})

    next_page = soup.find('div', {'class': 'cq-load-more primaryButton right'})
    if next_page:
        next_page = next_page.find_next('a').attrs['href']

laws = defaultdict(lambda: {})

for law in statutes:
    
    name, url = law.values()
    print(f'Processing {name}..')
    driver.get(f'{BASEURL}{url}')
    soup = BeautifulSoup(driver.page_source, 'lxml')

    laws[name]['url'] = url
    laws[name]['content'] = get_content(soup)

driver.close()

with open('data/laws_raw.json', 'w') as f:
    json.dump(laws, f)

print('time:', time.time() - start)
