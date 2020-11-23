#Author: Viswanath S Chirravuri
#Date: November 23, 2020

#This python script will perform unauthenticated traditional spidering on a given target website
#Pre-requisite: Python must be installed AND ZAP must be started and running on a listening port (like 8080 or 9090, etc.)

#If ZAP is not started yet, run the below command to start it (On LInux). This is a cross platform package so it can be used on Windows or MAC as well.
#$wget https://github.com/zaproxy/zaproxy/releases/download/v2.9.0/ZAP_2.9.0_Crossplatform.zip
#$unzip ZAP_2.9.0_Crossplatform.zip && cd ZAP_2.9.0
#$./zap.sh -host 0.0.0.0 -port 9090 -daemon -config api.key=mysecretapikey -nostdout -addonupdate -addoninstall ascanrulesBeta -addoninstall sqliplugin -addoninstall pscanrulesBeta -addoninstall ascanrulesAlpha -addoninstall domxss -addoninstall pscanrulesAlpha -addoninstall ascanrules -addoninstall pscanrules -addoninstall fuzzdb -addoninstall directorylistv2_3 -addoninstall directorylistv2_3_lc & 

#Official documentation on this script is available at https://github.com/zaproxy/zap-api-python/blob/master/src/examples/zap_example_api_script.py

#Install Python implementation of OWASP ZAP API (if it is not already done)
#pip3 install python-owasp-zap-v2.4

#!/usr/bin/env python3
import time
from zapv2 import ZAPv2 as ZAP
from pprint import pprint

# The URL of the application to be tested
target = 'https://demo.testfire.net/'

# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'mysecretapikey'
zap = ZAP(apikey=apiKey)

# By default ZAP API client will connect to port 8080
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
print("Started ZAP Scan")
zap = ZAP(apikey=apiKey, proxies={'http': 'http://127.0.0.1:9090', 'https': 'http://127.0.0.1:9090'})

# MANDATORY. True to create another ZAP session (overwrite the former if the same name already exists), False to use an existing one
isNewSession = True
# MANDATORY. ZAP Session name
sessionName = 'myappsession'

#Actual spidering starts here
print('Spidering target {}'.format(target))

# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')

# Optionally, print the URLs the spider has crawled
#print('\n'.join(map(str, zap.spider.results(scanID))))
