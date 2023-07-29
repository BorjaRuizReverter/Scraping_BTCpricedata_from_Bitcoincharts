# Scraping BTCpricedata from Bitcoincharts
This repository scrapes Bitcoin price data from the openwebsite Bitcoincharts.com

The purpose is to collect, clean and prepare Bitcoin price action data for further analysis.

## Installation
Make sure you are using the latest version of Python. Otherwise, download if from [here](https://www.python.org/downloads/)

After that install all the required packages:
```shell
pip install -r requirements.txt
```

You will also need a webdriver in order to the script manipulate the browser automaticly. Firefox, Internet Explorer, Safari, Opera, Chrome and Edge provide their own webdriver. However, the most reliable one is the GeckoDriver from Firefox. You will need both the browser and the webdriver, so download Firefox from [here](https://www.mozilla.org/en-US/firefox/new/) and the Geckodriver from [here](https://github.com/mozilla/geckodriver/releases), depending on your OS.

## Execution
Once you have all installed, you can clone this repository by open a terminal and typing:
```shell
git clone https://github.com/BorjaRuizReverter/Scraping_BTCpricedata_from_Bitcoincharts.git
```

Then move to the repository folder cloned:

```shell
cd Scraping_BTCpricedata_from_Bitcoincharts
```

and execute the python script
```shell
python3 ScrapingBTCpricedata.py
```
if you are in Linux, or

```shell
python ScrapingBTCpricedata.py
```
under Windows.
