#!/usr/bin/env python
# -*- coding: utf-8 -*-

from log_parser import LogParser
'''
    cn : callback name就代表广告播放的进度对吧
    n : network 代表网络，例如来自ESPN network
    adid : ad id
'''

class Processor:
    def __init__(self, parsed):
        self.metric = {
            #'IP': parsed.IP,
            #'datetime': parsed.datetime,
            'UA': parsed.UA
        }
        self.stats = {

        }

    def reduce(self):
        for ua in self.metric['UA']:
            if 'iPhone' in ua:
                self.stats['iPhone'] = self.stats.get('iPhone', 0) + 1;
            elif 'iPad' in ua:
                self.stats['iPad'] = self.stats.get('iPad', 0) + 1;
            elif 'Apple TV' in ua:
                self.stats['Apple TV'] = self.stats.get('Apple TV', 0) + 1;
            elif 'Android' in ua:
                self.stats['Android'] = self.stats.get('Android', 0) + 1;
            elif 'Mac' in ua:
                self.stats['Mac'] = self.stats.get('Mac', 0) + 1;
            elif 'Linux' in ua:
                self.stats['Linux'] = self.stats.get('Linux', 0) + 1;


if __name__ == '__main__':
    p = LogParser('log/prod-freewheel.espn.go.com.log')
    p.proceed()
    proc = Processor(p)
    proc.reduce()
    print proc.stats


