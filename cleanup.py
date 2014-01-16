#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    cleanup.py refactor the log_parser logics
               Produce a clean up logs.
'''


import re, bz2, datetime, time

class Cleaner:
    def __init__(self, input=None, output=None, max_line=-1, with_prefix=True, real_IP=True):
        self.file=input
        self.with_prefix=with_prefix
        self.real_IP=real_IP
        self.is_infinite=(max_line<0)
        self.max_line=max_line
        self.output=output



    def proceed(self):

        pattern = (r''
           '(\d+.\d+.\d+.\d+)\s.+\s-\s' #IP address
           '\[(.+)\]\s' #datetime
           '"((POST|HEAD|GET|PUT|DELETE|TRACE|CONNECT|OPTIONS))\s(.+)\s\w+/.+"\s(\d+)\s(\d+|-)'
           #requested file and HTTP code and file size(maybe not available)
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

        if self.with_prefix:
            pattern = '.+' + pattern

        if self.real_IP:
            pattern += '\s(\d+.\d+.\d+.\d+)'

        if '.bz' in self.file:
            f = bz2.BZ2File(self.file, 'r')
        else:
            f = open(self.file, 'r')

        if 'bz' in self.output:
            fout = bz2.BZ2File(self.output, 'w')
        else:
            fout = open(self.output, 'w')

        for line in f:
            IP, date_time, request, platform, app, method = self.parse(line, pattern, ua_list, app_category)
            fout.write(IP+', '+date_time+', '+request+', '+platform+', '+app+', '+method+'\n')
            #print(IP+', '+date_time+', '+request+', '+platform+', '+app+', '+method+'\n')
            if not self.is_infinite:
                self.max_line -= 1
                if self.max_line<=0:
                    break
        fout.close()
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
        #if "POST " in line or "HEAD " in line:
        #    return

        matched = self.find(pat, line, None)

        if matched:
            mat=matched[0]

            date_time=mat[1][:-6] # really dirty...
            if date_time:
                date_time=time.mktime(datetime.datetime.strptime(date_time, "%d/%b/%Y:%H:%M:%S").timetuple())
            request=mat[4]
            # HTTP code = mat[5]
            # Request size = mat[6]
            # Referrer = mat[7]
            IP = None
            if(self.real_IP):
                IP=mat[9]
            else:
                IP=mat[0]

            _ua = mat[8]

            find1, find2, ua_str, app_str = False, False, None, None
            for ua_str_ in ua_list:
                if ua_str_ in _ua:
                    find1 = True
                    ua_str = ua_str_
                    break

            for app in app_cat:
                if app in _ua:
                    find2 = True
                    app_str = app_cat[app]
                    break

            if not (find1 and find2):
                print('Unindentified UA: ' + _ua + '\noriginal line is: ' + line)

            method=mat[2] # mat[3] is the same

            return IP, str(date_time), request, str(ua_str), str(app_str), method
        else:
            raise NameError(line + ': Parsed error!')



    def find(self, pat, text, match_item):
        match = re.findall(pat, text)
        if match:
            return match
        else:
            return False

if __name__ == '__main__':

    p=Cleaner('./log/sample.log','./dump/sample_cleaned.log')
    p.proceed()
