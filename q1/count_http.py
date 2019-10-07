import re
from logParser import LogParser


logParser = LogParser('data/NASA_access_log_Aug95')
pattern = re.compile(r"\s+HTTP/[.0-9]+$")
count = 0
for log in logParser.read_log():
    if pattern.search(log['request']) is not None:
        count += 1

print("Number of HTTP requests = " + str(count))