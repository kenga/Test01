import re
import urllib.request
import json
from logParser import LogParser
from country_domain import country_domains


def query_country_code(ip_or_domain : str):
    url = "http://ip-api.com/json/" + ip_or_domain
    result = json.load(urllib.request.urlopen(url))
    if 'countryCode' in result:
        countryCode = result['countryCode'].lower()
        assert countryCode in country_domains
        return countryCode
    else:
        print("Failed to request country code for ", ip_or_domain)
        return None


logParser = LogParser('data/NASA_access_log_Aug95')
hostReqCounts = {}
for log in logParser.read_log():
    hostReqCounts[log['host']] = hostReqCounts.setdefault(log['host'], 0) + 1

ipReqCounts = {}
domainReqCounts = {}
countryReqCounts = {}
generalDomains = ['com', 'org', 'net', 'int', 'edu']
usDomains = ['gov', 'mil']

for hostReqCountPair in hostReqCounts.items():
    if re.match(r'\d+\.\d+\.\d+\.\d+', hostReqCountPair[0]) is not None:
        ipReqCounts[hostReqCountPair[0]] = hostReqCountPair[1]
    elif hostReqCountPair[0].endswith('.arpa'):
        continue
    else:
        match = re.search(r'(?P<whole>[\w\-]+\.(?P<top>\w+))$', hostReqCountPair[0])
        if match is not None:
            domainDict = match.groupdict()
            if domainDict['top'] in usDomains:
                countryReqCounts['us'] = countryReqCounts.setdefault('us', 0) + hostReqCountPair[1]
            elif domainDict['top'] in country_domains:
                thisCountryDomain = domainDict['top']
                countryReqCounts[thisCountryDomain] = countryReqCounts.setdefault(thisCountryDomain, 0) + hostReqCountPair[1]
            elif domainDict['top'] in generalDomains:
                domainReqCounts[domainDict['whole']] = domainReqCounts.setdefault(domainDict['whole'], 0) + hostReqCountPair[1]

print("Querying country code for domains and IP addresses...")
for domainReqCountPair in list(domainReqCounts.items()) + list(ipReqCounts.items()):
    countryCode = query_country_code(domainReqCountPair[0])
    if countryCode is not None:
        countryReqCounts[countryCode] = countryReqCounts.setdefault(countryCode, 0) + domainReqCountPair[1]

topCountryReqCount = sorted(countryReqCounts.items(), key=lambda x: x[1], reverse=True)[0]
print("Top country with most request: %s  (no. of request = %d)" %
      (country_domains[topCountryReqCount[0]], topCountryReqCount[1]))

