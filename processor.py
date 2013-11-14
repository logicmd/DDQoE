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
            'iPhone': 0
            'iPad': 0
            'UA': 0
            'ATV': 0
        }

    def reduce(self):
        for ua in self.metric['UA']:
            if 'iPhone' in ua:
                self.stats['iPhone'] += 1;
            if 'iPad' in ua:
                self.stats['iPad'] += 1;
            if 'Mac OS' in ua:
                self.stats['Mac'] += 1;
            if 'TV' in ua:
                self.stats['ATV'] += 1;




if __name__ == '__main__':
    p = LogParser('log/prod-freewheel.espn.go.com.log')
    p.proceed()
    proc = Processor(p)
    proc.reduce()
    print proc.stats


