from datetime import date

#Data scraped is from one day before start_date
start_date = date(2017, 7, 2)
end_date = date(2017, 7, 4)

#Some of the exchanges are: bitfinex, bitstamp, kraken, mtgox, ...
exchange = 'kraken'

#Some of the currencies are: USD, EUR, CAD, BRL, ...
currency = 'USD'

exchangeAndCurrency = exchange + currency

from selenium import webdriver
#Choose de webdriver
#driver = webdriver.Chrome()
#driver = webdriver.Chrome(desired_capabilities=capabilities)
driver = webdriver.Firefox()