#Author: Viswanath S Chirravuri
#Date: November 23, 2020

#This python script will perform unauthenticated traditional spidering on a given target website
#Pre-requisite: Python must be installed AND ZAP must be started and running on a listening port (like 8080 or 9090, etc.)

#If ZAP is not started yet, run the below command to start it (On LInux). This is a cross platform package so it can be used on Windows or MAC as well.
#$wget https://github.com/zaproxy/zaproxy/releases/download/v2.9.0/ZAP_2.9.0_Crossplatform.zip
#$unzip ZAP_2.9.0_Crossplatform.zip && cd ZAP_2.9.0
#$./zap.sh -host 0.0.0.0 -port 9090 -daemon -config api.key=mysecretapikey -nostdout -addonupdate -addoninstall ascanrulesBeta -addoninstall sqliplugin -addoninstall pscanrulesBeta -addoninstall ascanrulesAlpha -addoninstall domxss -addoninstall pscanrulesAlpha -addoninstall ascanrules -addoninstall pscanrules -addoninstall fuzzdb -addoninstall directorylistv2_3 -addoninstall directorylistv2_3_lc & 

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import os

opts = Options()
opts.headless = True

PROXY = "localhost:9091"
webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",
}

driver = webdriver.Firefox(options=opts)

target = 'https://demo.testfire.net'

try:
    # spider the URL's
    driver.get(target + '/login.jsp')
    time.sleep(1)

    driver.get(target + "/feedback.jsp")
    time.sleep(1)

    driver.get(target + "/search.jsp?query=jsmith")
    time.sleep(1)

    driver.get(target + "/doSubscribe")
    time.sleep(1)

    driver.get(target + "/subscribe.jsp")
    time.sleep(1)

finally:
    driver.close()

