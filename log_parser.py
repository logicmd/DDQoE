#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    parser.py是系统模块的名字
'''

import re
from request import Request

class LogParser:
    def __init__(self, file_name=None):
        self.file=file_name
        self.request=[]
        self.IP=[]
        self.datetime=[]
        self.size=[]
        self.UA=[]


    def proceed(self):
        for line in open(self.file, 'r'):
            self.parse(line)

        #self.parse(open(self.file, 'r').read())

    '''
        re.findall的写法要求对每一行都把所有组成部分的正则表达式子都写出来，
        括号里面标注要match输出的

        pattern = (r ''
            'rexp1'
            'rexp2'
            'rexp3'
            )

        re.findall(pattern, text)

        re.compile/search的写法保证把特定rexp的k个匹配找出来，不适合多个pattern
        分别匹配的情景
        rexp=re.compile('')
        match=rexp.search(text)
        match.group(k)

    '''

    def parse(self, line):
        pat = (r''
           '(\d+.\d+.\d+.\d+)\s.+\s-\s' #IP address
           '\[(.+)\]\s' #datetime
           '"GET\s(.+)\s\w+/.+"\s(\d+)\s(\d+)' #requested file and HTTP code and file size
           '\s"(.+)"\s' #referrer
           '"(.+)"' #user agent
        )
        matched = self.find(pat, line, None)
        #print matched

        self.IP.append(matched[0][0]);
        self.datetime.append(matched[0][1]);
        self.datetime.append(matched[0][4]);
        self.UA.append(matched[0][6]);

        areq = Request(matched[0][0], matched[0][1], matched[0][4], matched[0][6])
        #print areq



    def find(self, pat, text, match_item):
        match = re.findall(pat, text)
        if match:
            return match
        else:
            return False

if __name__ == '__main__':

    p=Parser('log/prod-freewheel.espn.go.com-head.log')
    p.proceed()

