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

#Data scraped is from one day before start_date
'''
#BITFINEX
exchange = 'bitfinexUSD'
start_date = date(2019, 9, 3)
end_date = date(2019, 9, 10)
'''
'''
#BITSTAMP
exchange = 'bitstampUSD'
start_date = date(2019, 6, 3)
end_date = date(2019, 11, 25)
'''
#KRAKEN
exchange = 'krakenUSD'
start_date = date(2017, 7, 2)
end_date = date(2017, 7, 4)
#end_date = date(2014, 1, 12)
'''
#MTGOX
exchange = 'mtgoxUSD'
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
    proxies = get_proxies()
    #len(proxies)
    #PROXY = random.sample(proxies, 1) #It seems deprecated from Python 3.9
    PROXY = random.sample(list(proxies), 1)
except:
    #Sometimes get_proxies doesnt work. In that case, access https://free-proxy-list.net/ and take a fixed PROXY
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
    year_str = start_date.strftime("%Y-%m-%d")[0:4]
    month_str = start_date.strftime("%Y-%m-%d")[5:7]
    day_str = start_date.strftime("%Y-%m-%d")[8:10]

    start_date += delta
    urls.append('https://bitcoincharts.com/charts/'+exchange+'#rg1zig1-minzczsg'+year_str+'-'
                +month_str+'-'+day_str+'zeg'+year_str+'-'+month_str+'-'+day_str+'ztgSzm1g10zm2g25zv')

    # Access the webpage
    #chrome.get(urls[loop_number])
    driver.get(urls[loop_number])
    driver.refresh()

    try:
        #element = driver.find_element_by_link_text('Load raw data') #It was deprecated
        element = driver.find_element(By.LINK_TEXT, 'Load raw data')
        driver.execute_script("arguments[0].click();", element)
    except:  
        print("Error in Element")
        while internet()==False:
        #Wait for the internet to come back
            for j in range(10,0,-1):
                import time
                time.sleep(1)
                print('Internet is down. Retrying in', j, 'seconds')
            print('Retrying connection...')
            #import time
            #random_number = random.sample(range(1,10),1)
            #time.sleep(3+random_number[0])
            driver.refresh()
            #element = driver.find_element_by_link_text('Load raw data') #It was deprecated
            element = driver.find_element(By.LINK_TEXT, 'Load raw data')
            driver.execute_script("arguments[0].click();", element)
    
    ActionChains(driver).click().perform()
    
    #After clicking the button the site lasts a bit to load. That is why we pause the script for seconds.
    import time
    random_number = random.sample(range(1,10),1)
    time.sleep(4+random_number[0])

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find(name='table', attrs={'id':'chart_table'})
    table2 = pd.read_html(str(table))[0]
    #table2 = table2.drop(1440) #We remove the last row because it repeats with the first one of the day after
    table2 = table2.drop(0) #We remove the last row because it repeats with the last one of the day after
    table2 = table2.replace('—', 'NaN')

    try:
        print(table2.Timestamp[1])
    except:
        print("Data gap")

    #df = df.append(table2, ignore_index=True) #append will be deprecated, so we substituted for concat below
    df = pd.concat([df, table2], ignore_index=True)

    loop_number = loop_number + 1

driver.close()

df.to_csv(r'Scraped_data.csv', index=False)
#We transform the column time from Timestamp to TimeIndex
df_timeindex = df
df_timeindex['Timestamp']=pd.DatetimeIndex(df_timeindex.Timestamp).asi8//10 ** 9
df_timeindex.to_csv(r'Scraped_data_in_timeindex.csv', index=False)
