# Following are the scripts to be used to perform the following tasks using OWASP ZAP
1. Traditional Spidering
2. AJAX Spidering
3. Passive Scan
4. Active Scan

Note: ZAP must be pre-installed and running on specific port. 

## [Python] Command to run the scripts
Note 1: Python must be pre-installed prior to running the script.

Note 2: You have to edit the Python script to update the ZAP listening port, if the port is not 9090.
### For Traditional Spidering
$python3 Python/traditional_spidering.py
### For Integration with QA tests with Selenium and Firefox
$python3 Python/qa-tests-with-selenium.py
