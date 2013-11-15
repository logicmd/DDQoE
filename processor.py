#!/usr/bin/env python
# -*- coding: utf-8 -*-

from log_parser import LogParser
'''
    cn : callback name就代表广告播放的进度
    n : network 代表网络，reseller network id(s), content right owner network id
    adid : ad id

    progress
    slotImpression:slotEnd
    defaultImpression:firstQuartile:midPoint:thirdQuartile:complete:adEnd
    _e_renderer-load、_e_unknown



'''

class Processor:
    def __init__(self, parsed):
        self.metric = {
            #'IP': parsed.IP,
            #'datetime': parsed.datetime,
            'UA': parsed.UA,
            'request': parsed.request
        }
        self.stats = {

        }

        self.m3u8 = []

        progress = {
            # 'complete': ,
            # 'adEnd': ,
            # 'slotEnd': ,
        }

    def reduce(self):
        self.stats['Platform'] = {}
        platform = self.stats['Platform']

        self.stats['App'] = {}
        app = self.stats['App']

        for ua in self.metric['UA']:

            if 'iPhone' in ua:
                platform['iPhone'] = platform.get('iPhone', 0) + 1;
            elif 'iPad' in ua:
                platform['iPad'] = platform.get('iPad', 0) + 1;
            elif 'Apple TV' in ua:
                platform['Apple TV'] = platform.get('Apple TV', 0) + 1;
            elif 'Android' in ua:
                platform['Android'] = platform.get('Android', 0) + 1;
            elif 'Mac' in ua:
                platform['Mac'] = platform.get('Mac', 0) + 1;
            elif 'Linux' in ua:
                platform['Linux'] = platform.get('Linux', 0) + 1;


            if 'Mozilla' in ua:
                app['ThirdParty'] = app.get('ThirdParty', 0) + 1;
            elif 'AppleCoreMedia' in ua:
                app['Native'] = app.get('Native', 0) + 1;



        self.stats['Ad'] = {}
        ad = self.stats['Ad']

        self.stats['Progress'] = {}
        progress = self.stats['Progress']

        for req in self.metric['request']:
            raw_id = self.get_quartile(req, 'adid');
            if raw_id:
                adid = int(raw_id);
                ad[adid] = ad.get(adid, 0) + 1;

            raw_progress = self.get_quartile(req, 'cn');
            if raw_progress:
                prog = raw_progress;
                progress[prog] = progress.get(prog, 0) + 1;

            raw_m3u8_url = self.get_quartile(req, '_fw_lpu');

            if raw_m3u8_url:
                print raw_m3u8_url
                break
                m3u8_url = raw_m3u8_url.replace('%3A',':');
                self.m3u8.append(m3u8_url)






    # def get_progress(self, text):


    def get_quartile(self, text, tagname):
        st_ind = text.find('&' + tagname + '=')
        en_ind = text[st_ind+len(tagname):].find('&')
        if st_ind>-1:
            if en_ind>-1:
                return text[st_ind+len(tagname)+2:st_ind+len(tagname)+en_ind]
            else:
                return text[st_ind+6:]

if __name__ == '__main__':
    p = LogParser('log/prod-freewheel.espn.go.com.log')
    p.proceed()
    proc = Processor(p)
    proc.reduce()
    print len(proc.stats['Ad'])
    for metric in proc.stats:
        print metric+ ': '
        print proc.stats[metric]
    #print proc.m3u8

