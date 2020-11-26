# Author: Viswanath S Chirravuri (chvasu)
# Date: November 23, 2020

# This python script will perform unauthenticated traditional spidering on a given target website
# Pre-requisite: Python must be installed AND ZAP must be started and running on a listening port (like 8080 or 9090, etc.)

# If ZAP is not started yet, run the below command to start it (On LInux). This is a cross platform package so it can be used on Windows or MAC as well.
# $wget https://github.com/zaproxy/zaproxy/releases/download/v2.9.0/ZAP_2.9.0_Crossplatform.zip
# $unzip ZAP_2.9.0_Crossplatform.zip && cd ZAP_2.9.0
# $./zap.sh -host 0.0.0.0 -port 9090 -daemon -config api.key=mysecretapikey -nostdout -addonupdate -addoninstall ascanrulesBeta -addoninstall sqliplugin -addoninstall pscanrulesBeta -addoninstall ascanrulesAlpha -addoninstall domxss -addoninstall pscanrulesAlpha -addoninstall ascanrules -addoninstall pscanrules -addoninstall fuzzdb -addoninstall directorylistv2_3 -addoninstall directorylistv2_3_lc &

# Official documentation on this script is available at https://github.com/zaproxy/zap-api-python/blob/master/src/examples/zap_example_api_script.py

# Install Python implementation of OWASP ZAP API (if it is not already done)
# pip3 install python-owasp-zap-v2.4

# !/usr/bin/env python3
import json
import urllib.parse

# The URL of the application to be tested
target = 'http://redacted.com/'

# Get Alert summary
headers = {
  'Accept': 'application/json',
  'X-ZAP-API-Key': 'mysecretapikey',
  'baseurl': urllib.parse.quote_plus(target)
}
r = requests.get('http://zapserver:9090/JSON/alert/view/alertsSummary/', params={
}, headers = headers)
data = r.json()
if data['alertsSummary']['High'] == 0:
    print('Pass the build!')  
else:
    print('Fail the build!')
