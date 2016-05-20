"""Fetch logs from a Motorola SB6141 Cable modem."""

import argparse
import time
import urllib.request

from bs4 import BeautifulSoup


class Foo(object):
    def __init__(self, items=None, stateSize=100):
        if items is None:
            self.items = []
        else:
            self.items = items
        self.stateSize = stateSize

    def update(self, items):
        tocompare = self.items[-len(items):]
        matched = items
        added = []

        while tocompare != matched:
            tocompare = tocompare[1:]
            added = [matched.pop()] + added
        self.items = (self.items + added)[-self.stateSize:]
        return added

    def getState(self):
        return self.lines


class LogFetcher(object):
    def __init__(self, url='http://192.168.100.1/cmLogsData.htm'):
        self.url = url

    def fetch(self):
        with urllib.request.urlopen(self.url) as f:
            data = f.read().decode('utf-8')
            soup = BeautifulSoup(data, 'html.parser')
            log_data = []
            for log_row in soup.table.find_all('tr'):
                cols = [c.string for c in log_row.find_all('td')]
                if len(cols) != 4:
                    continue
                log_data.append(cols)
            log_data.reverse()
            return log_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch logs from SB6141.')
    parser.add_argument('--state', default='/var/run/sblog.state',
                        help='where to store state between runs')
    parser.add_argument('--url', default='http://192.168.100.1/cmLogsData.htm',
                        help='url for modem logs')
    parser.add_argument('--out', help='file to append log entries to')

    args = parser.parse_args()
    f = LogFetcher(url=args.url)
    logs = Foo()
    while True:
        try:
            print('Fetching...')
            new_logs = logs.update(f.fetch())

            for log_row in new_logs:
                print(' '.join(log_row))
        except urllib.error.URLError:
            pass

        time.sleep(10)
