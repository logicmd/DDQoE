#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    parser.py是系统模块的名字
'''

import re, cPickle, bz2
from request import Request

class LogParser:
    def __init__(self, file_name=None, max_line=-1):
        self.file=file_name
        self.request=[]
        self.IP=[]
        self.datetime=[]
        self.size=[]
        self.UA=[]
        self.platform=[]
        self.app=[]
        self.is_bz="bz" in self.file
        self.is_full=self.is_bz or "full" in self.file
        self.is_infinite=(max_line<0)
        self.max_line=max_line



    def proceed(self):

        pattern = (r''
           '(\d+.\d+.\d+.\d+)\s.+\s-\s' #IP address
           '\[(.+)\]\s' #datetime
           '"GET\s(.+)\s\w+/.+"\s(\d+)\s(\d+|-)' #requested file and HTTP code and
                                                #file size(maybe not available)
           '\s"(.+)"\s' #referrer
           '"(.+)"' #user agent
        )

        ua_list = [
            'Xbox', 'Windows', 'CrOS',
            'iPod', 'Wii', 'PS', 'NativeHost',
            'iPhone', 'iPad', 'Apple TV',
            'Android', 'Mac', 'Linux'
            ]

        app_category = {
            'Mozilla': 'BrowserThirdParty',
            'AppleCoreMedia': 'AppleNative',
            'VisualOn': 'VisualOnThirdParty',
            'Xbox': 'XboxNative',
            'youtube': 'YoutubeThirdParty'
            }

        if self.is_bz:
            pattern = '.+:' + pattern

        if self.is_full:
            pattern += '\s(\d+.\d+.\d+.\d+)'

        if '.bz' in self.file:
            f = bz2.BZ2File(self.file)
        else:
            f = open(self.file, 'r')

        for line in f:
            self.parse(line, pattern, ua_list, app_category)

            if not self.is_infinite:
                self.max_line -= 1
                if self.max_line<=0:
                    break


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

    def parse(self, line, pat, ua_list, app_cat):

        matched = self.find(pat, line, None)
        if matched:
            self.datetime.append(matched[0][1])
            self.request.append(matched[0][2])
            if(self.is_full):
                self.IP.append(matched[0][7])
            else:
                self.IP.append(matched[0][0])

            _ua = matched[0][6]
            self.UA.append(_ua)

            find = False
            for ua_str in ua_list:
                if ua_str in _ua:
                    self.platform.append(ua_str)
                    find = True
                    break

            for app in app_cat:
                if app in _ua:
                    self.app.append(app_cat[app])

                    break

            if not find:
                print _ua
            print matched[0][7], matched[0][1], matched[0][4], matched[0][6]
        else:
            print line
            raise NameError("parsed error")



    def find(self, pat, text, match_item):
        match = re.findall(pat, text)
        if match:
            return match
        else:
            return False

if __name__ == '__main__':

    p=LogParser('log/prod-freewheel.espn.go.com.log.bz2', 5)
    p.proceed()
    if not len(p.datetime) == len(p.request) == len(p.UA) == len(p.platform) == len(p.app):
        raise IndexError
    f=open('dump/parsed','wb')
    cPickle.dump(p, f, True)
    f.close()

