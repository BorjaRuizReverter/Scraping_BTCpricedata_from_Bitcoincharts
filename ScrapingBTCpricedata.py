import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml.html import fromstring
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date, timedelta

from selenium.webdriver.common.by import By

urls = []
df = pd.DataFrame([])

#Os dados baixados do site se correspondem com um dia antes do start_date
'''
#BITFINEX
correitora = 'bitfinexUSD'
start_date = date(2019, 9, 3)
end_date = date(2019, 9, 10)
'''
'''
#BITSTAMP
correitora = 'bitstampUSD'
start_date = date(2019, 6, 3)
end_date = date(2019, 11, 25)
'''
#KRAKEN
correitora = 'krakenUSD'
start_date = date(2017, 7, 2)
end_date = date(2017, 7, 4)
#end_date = date(2014, 1, 12)
'''
#MTGOX
correitora = 'mtgoxUSD'
start_date = date(2011, 6, 28)
end_date = date(2014, 2, 24)
'''

delta = timedelta(days=1)

def internet():
    try:
        urlopen('https://www.google.com.br', timeout=1)
        return True
    except Exception as ex:
        return False

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

try: 
    proxies = get_proxies()#Usamos a função definida acima
    #len(proxies)
    #PROXY = random.sample(proxies, 1)#It seems deprecated from Python 3.9
    PROXY = random.sample(list(proxies), 1)
except:
    #A função get_proxies não funciona as vezes. Nesse caso, entrar no site https://free-proxy-list.net/ e pegar um PROXY fixo 
    PROXY = '175.100.30.156:25'

capabilities = webdriver.DesiredCapabilities.CHROME['proxy']={
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "autodetect":False,
    'verify_ssl': False
}
#driver = webdriver.Chrome(desired_capabilities=capabilities)
#driver = webdriver.Chrome()
driver = webdriver.Firefox()

loop_number = 0
while start_date <= end_date:
    #print (start_date.strftime("%Y-%m-%d"))
    start_date.strftime("%Y-%m-%d")
    ano_str = start_date.strftime("%Y-%m-%d")[0:4]
    mes_str = start_date.strftime("%Y-%m-%d")[5:7]
    dia_str = start_date.strftime("%Y-%m-%d")[8:10]

    start_date += delta
    urls.append('https://bitcoincharts.com/charts/'+correitora+'#rg1zig1-minzczsg'+ano_str+'-'
                +mes_str+'-'+dia_str+'zeg'+ano_str+'-'+mes_str+'-'+dia_str+'ztgSzm1g10zm2g25zv')

    # Access the webpage
    #chrome.get(urls[loop_number])
    driver.get(urls[loop_number])
    driver.refresh()

    try:
        #element = driver.find_element_by_link_text('Load raw data') #It was deprecated
        element = driver.find_element(By.LINK_TEXT, 'Load raw data')
        driver.execute_script("arguments[0].click();", element)
    except:  
        print("ERROR DE ELEMENT")
        while internet()==False:
        #Wait for the internet to come back
            for j in range(10,0,-1):
                import time
                time.sleep(1)
                print('Internet is down. Retrying in', j, 'seconds')
            print('Retrying connection...')
            #import time
            #num_aleatorio = random.sample(range(1,10),1)
            #time.sleep(3+num_aleatorio[0])
            driver.refresh()
            #element = driver.find_element_by_link_text('Load raw data') #It was deprecated
            element = driver.find_element(By.LINK_TEXT, 'Load raw data')
            driver.execute_script("arguments[0].click();", element)
    
    ActionChains(driver).click().perform()
    
    #Após clicar no botão o site demora em carregar. Por isso vamos pausar o script uns segundos.
    import time
    num_aleatorio = random.sample(range(1,10),1)
    time.sleep(4+num_aleatorio[0])

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find(name='table', attrs={'id':'chart_table'})
    tabela = pd.read_html(str(table))[0]
    #tabela = tabela.drop(1440) #Tiramos a última fila porque se repete com a primeira do dia seguinte
    tabela = tabela.drop(0) #Tiramos a última fila porque se repete com a última do dia anterior
    tabela = tabela.replace('—', 'NaN')

    try:
        print(tabela.Timestamp[1])
    except:
        print("Lacuna de dados")

    #df = df.append(tabela, ignore_index=True) #append will be deprecated, so we substituted for concat below
    df = pd.concat([df, tabela], ignore_index=True)

    loop_number = loop_number + 1

driver.close()

df.to_csv(r'Scraped_data.csv', index=False)
#Transformamos a coluna do tempo de Timestamp para TimeIndex
df_timeindex = df
df_timeindex['Timestamp']=pd.DatetimeIndex(df_timeindex.Timestamp).asi8//10 ** 9
df_timeindex.to_csv(r'Scraped_data_in_timeindex.csv', index=False)
