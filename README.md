# Following are the scripts to be used to perform the following tasks using OWASP ZAP
1. Traditional Spidering
2. AJAX Spidering
3. Passive Scan
4. Active Scan

Note: ZAP must be pre-installed and running on specific port. 

## [Python] Command to run the scripts
Note 1: Python must be pre-installed prior to running the script.

Note 2: You have to edit the Python script to update the ZAP listening port, if the port is not 9090.
### For spidering, passive scan, active scan, making HTML report
$python3 Python/zap_spider_passive_active_scan_with_report.py
### For Integration with QA tests with Selenium and Firefox
$python3 Python/qa-tests-with-selenium.py

## [Java] Command to run the code
Note 1: JDK or JRE must be pre-installed prior to running the code.

Note 2: You have to edit the Java code to update ZAP listening post, if the port is not 9090. And update for ZAP host, and the target URL.
### For spidering, passive scan, active scan, making HTML report
$javac Java/Java_ZAP_client.java && java Java_ZAP_client
