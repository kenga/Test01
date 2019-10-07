from datetime import datetime
from logParser import LogParser


logParser = LogParser('data/NASA_access_log_Aug95')
timeFormat = '%d/%b/%Y:%H:%M:%S %z'
beginTime = datetime.strptime('18/Aug/1995:00:00:00 -0400', timeFormat)
endTime = datetime.strptime('21/Aug/1995:00:00:00 -0400', timeFormat)

hostReqCount = {}
for log in logParser.read_log():
    logTime = datetime.strptime(log['time'], timeFormat)
    if beginTime <= logTime < endTime:
        hostReqCount[log['host']] = hostReqCount.setdefault(log['host'], 0) + 1

print("top 10 hosts makes most request:")
print('Req Count | Host')
print('==========================')
for item in sorted(hostReqCount.items(), key=lambda x: x[1], reverse=True)[:10]:
    print("%8d    %s" % (item[1], item[0]))
