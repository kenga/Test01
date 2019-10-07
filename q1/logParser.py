import re


class LogParser:
    logPattern = re.compile(
        r'^\s*(?P<host>\S+)\s+' +
        r'(?P<client_id>\S+)\s+' +
        r'(?P<user>\S+)\s+' +
        r'\[(?P<time>.+)\]\s+' +
        r'"(?P<request>.*)"\s+' +
        r'(?P<status>\d+)\s+' +
        r'(?P<size>\S+)\s*$'  # size can be '-'
    )
    logFile = None

    def __init__(self, logFilePath):
        self.logFile = open(logFilePath, 'r', encoding="utf-8", errors="ignore")

    def __del__(self):
        self.logFile.close()

    def read_log(self):
        """
        yield one line of log at a time
        :return:
        """
        for line in self.logFile:
            yield self.logPattern.match(line).groupdict()


if __name__ == "__main__":
    # todo: test case (example code showing usage)
    logParser = LogParser('data/NASA_access_log_Aug95')
    count = 0
    for log in logParser.read_log():
        print(log)
        count += 1
        if count > 10:
            break
