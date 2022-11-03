from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import time

_options = Options()
_options.add_argument('--headless')
_driver = webdriver.Chrome(ChromeDriverManager().install(), options=_options)

# define needed information
_repo_name = []
_repo_url = []
_language = []
_proj_description = []
_star_count = [] # this is going to be used for the Hacktoberfest links

#print(repo_name)
#print(repo_url)
#print(language)

# hacktoberfest variables
_recordcount = 0
_pagecount = 1

    
def FetchFromGoodFirstIssue(url):
    # set url to fetch data from
    _driver.get(url)

    # initialize selenium and beautifulsoup
    content = _driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # repo name, project url, can be fetched here
    for a in soup.findAll('div', attrs={'class':'flex flex-row'}):
        reponame = a.find('a', attrs={'class' : 'text-xl font-bold group-hover:text-juniper'})
        repourl = a.find('a', attrs={'class' : 'text-xl font-bold group-hover:text-juniper'}).get('href')
        _repo_name.append(reponame.text)
        _repo_url.append(repourl)

    # repo lang can be fetched here since it's under a different tag
    for b in soup.findAll('div', attrs={'class' : 'flex-row flex text-sm py-1 font-mono text-vanilla-400'}):
        repolang = b.find('div', attrs={'class' : 'mr-4'})
        raw_lang = str(repolang.text)
        extracted_lang = raw_lang.lstrip('lang: ')
        _language.append(extracted_lang)

    # here is desc since this is under a different tag
    for c in soup.findAll('div', attrs={'class' : 'flex-row flex text-sm py-1 overflow-auto'}):
        raw_str = str(c.text)
        remove_newline = raw_str.replace('\n', '')
        str_spacesremoved = remove_newline.lstrip('      ')
        _proj_description.append(str_spacesremoved)

    _ExportToCSV('GoodFirstIssue')

def FetchFromUpForGrabs(url):
    # set url to fetch data from
    _driver.get(url)
    print('Loading site and fetching data...')
    time.sleep(5)

    # initialize selenium and beautifulsoup
    content = _driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # repo name, project url, can be fetched here
    for a in soup.findAll('span', attrs={'class':'proj'}):
        reponame = a.find('a')
        repourl = a.find('a').get('href')
        _repo_name.append(reponame.text)
        _repo_url.append(repourl)

    # repo desc can be fetched here since it's under a different tag
    for b in soup.findAll('span', attrs={'class' : 'desc'}):
        repodesc = b.find('p')
        _proj_description.append(repodesc.text)

    # here is desc since this is under a different tag
    for c in soup.findAll('p', attrs={'class' : 'tags'}):
        projlang = c.find('a')
        _language.append(projlang.text)

    _ExportToCSV('UpForGrabs')

def FetchFromHacktoberfest(lang):
    #_FetchHacktoberfest(lang)
    rcount = _GetRecordCountHacktoberfest(lang)
    _FetchHacktoberfest(lang, rcount)

def _GetRecordCountHacktoberfest(lang):
    print('Getting record count...')
    # set url to fetch data from
    _driver.get('https://hacktoberfest-projects.vercel.app/repos/' + lang + '?p=1')

    # initialize selenium and beautifulsoup
    content = _driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    count = soup.find('h1', attrs={'class' : 'mb-5 text-5xl font-bold'})
    raw = str(count.text)
    rec_count = int(raw.replace(' repositories for ' + lang, ''))
    return rec_count

def _FetchHacktoberfest(l, c):
    print('Fetching records...')
    _loopstep = 21
    _page = 1
    # run the loop while recordcount 
    for x in range(0 ,c, _loopstep):

        # set url to fetch data from
        _driver.get('https://hacktoberfest-projects.vercel.app/repos/' + l + '?p=' + str(_page))
        print('accessing page https://hacktoberfest-projects.vercel.app/repos/' + l + '?p=' + str(_page))
        time.sleep(5) # implement delay for the page to load properly
        
        # initialize selenium and beautifulsoup
        content = _driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        # repo name, project url, can be fetched here
        for a in soup.findAll('div', attrs={'class':'shadow-sm card bg-base-300 mx-4'}):
            reponame = a.find('a', attrs={'class' : 'text-3xl card-title link link-hover text-primary'})
            repourl = a.find('a', attrs={'class' : 'text-3xl card-title link link-hover text-primary'}).get('href')
            stars = a.find('div', attrs={'class' : 'text-center stat-value'})
            _repo_name.append(reponame.text)
            _repo_url.append(repourl)
            _language.append(l)
            _star_count.append(stars.text)
            
        #_driver.close() # attempt to close the driver so that it can be reopened
        _page += 1
        

    _ExportCSV_Hacktoberfest(l)


def _ExportToCSV(filename):
    # Save information to a CSV file
    df = pd.DataFrame({'Repo Name' : _repo_name, 'Repo URL' : _repo_url, 'Language' : _language, 'Description' : _proj_description})
    df.to_csv('repos ' + filename + '.csv', index = False, encoding='utf-8')
    print('Extracted data saved locally.')

def _ExportCSV_Hacktoberfest(lang):
    # Save information to a CSV file
    df = pd.DataFrame({'Stars' : _star_count, 'Repo Name' : _repo_name, 'Repo URL' : _repo_url, 'Language' : _language})
    df.to_csv('reposhacktoberfest' + lang + '.csv', index = False, encoding='utf-8')
    print('Extracted data saved locally.')
