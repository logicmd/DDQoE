#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, cPickle, os
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
            'UA'        : parsed.UA,
            'request'   : parsed.request,
            'platform'  : parsed.platform,
            'app'       : parsed.app,
            'IP'        : parsed.IP,
            'time'      : parsed.datetime
        }
        self.stats = {

        }

        self.m3u8 = []

        progress = {
            # 'complete': ,
            # 'adEnd': ,
            # 'slotEnd': ,
        }


        self.quality = {

        }
        self.quality['ad'] = {}
        self.quality['content'] = {}

        self.behavior = {}
        self.ip_dict = {}

    def reduce(self):
        self.stats['Platform'] = {}
        platform = self.stats['Platform']

        self.stats['App'] = {}
        app = self.stats['App']


        for p in self.metric['platform']:
            platform[p] = platform.get(p, 0) + 1

        for a in self.metric['app']:
            app[a] = app.get(a, 0) + 1


        self.stats['Ad'] = {}
        ad = self.stats['Ad']

        self.stats['Progress'] = {}
        progress = self.stats['Progress']


        c = -1
        for req in self.metric['request']:
            c+=1
            ad_behave = ''
            raw_id = self.get_quartile(req, 'adid');
            if raw_id:
                ad_behave+=raw_id
                adid = int(raw_id);
                ad[adid] = ad.get(adid, 0) + 1;

            raw_progress = self.get_quartile(req, 'cn');
            if raw_progress:
                ad_behave+=(': '+raw_progress)
                prog = raw_progress;
                progress[prog] = progress.get(prog, 0) + 1;

            bitrate = 0
            raw_m3u8_url = self.get_quartile(req, '_fw_lpu')
            if raw_m3u8_url:
                m3u8_url = raw_m3u8_url.replace('%3A',':')
                self.m3u8.append(m3u8_url)
                bitrate = self.get_quality(m3u8_url)

            if bitrate == 'master':
                behave = str(bitrate) + '; ' + ad_behave
            else:
                behave = str(bitrate) + 'kbps' + '; ' + ad_behave

            if bitrate==0 and ad_behave=='':
                #print req
                pass

            time = self.get_time(self.metric['time'][c])
            self.update_behavior(
                self.metric['IP'][c],
                self.metric['platform'][c],
                self.metric['app'][c],
                time,
                behave
                )

            #if ''
            self.update_ip_dict(
                self.metric['IP'][c],
                self.metric['platform'][c],
                self.metric['app'][c]
                )


    def get_quality(self, url):

        br = None

        if 'ads' in url:
            if 'master' in url:
                br = 'master'
                self.quality['master'] = self.quality.get('master', 0) + 1
            else:
                rexp=re.compile('/\d+K/')
                match=rexp.search(url)
                if match:
                    br = int(match.group(0).replace('/','').replace('K',''))
                    bitrate = br #str(br) + 'kbps'
                    self.quality['ad'][bitrate] = self.quality['ad'].get(bitrate, 0) + 1
                else:
                    print url
                    self.quality['unknown'] = self.quality.get('unknown', 0) + 1
                    raise IndexError

        elif '-' in url:
            rexp=re.compile('-\d+(_audio)?.m3u8')
            match=rexp.search(url)

            if match:
                raw_str = match.group(0)
                strip_str = []
                for char in raw_str:
                    if char >= '0' and char <= '9':
                        strip_str.append(char)
                    if char == '.':
                        break

                br = int(''.join(strip_str))
                bitrate = br
                self.quality['content'][bitrate] = self.quality['content'].get(bitrate, 0) + 1

            elif 'tablet' in url or 'mobile' in url:
                br = 'master'
                self.quality['master'] = self.quality.get('master', 0) + 1
            else:
                print url
                self.quality['unknown'] = self.quality.get('unknown', 0) + 1
                raise IndexError

        else:
            print url
            self.quality['unknown'] = self.quality.get('unknown', 0) + 1
            raise IndexError

        return br

    # def get_progress(self, text):


    def get_quartile(self, text, tagname):
        st_ind = text.find('&' + tagname + '=')
        en_ind = text[st_ind+len(tagname):].find('&')
        if st_ind>-1:
            if en_ind>-1:
                return text[st_ind+len(tagname)+2:st_ind+len(tagname)+en_ind]
            else:
                return text[st_ind+len(tagname)+2:]


    def update_behavior(self, ip, platform, app, time, bitrate):
        user = ip + '-' + platform #+ '-' + app
        if user not in self.behavior:
            self.behavior[user] = []

        behavior = (time, bitrate)
        self.behavior[user].append(behavior)

    def update_ip_dict(self, ip, platform, app):
        identifying = ip #+ '-' + app
        if identifying not in self.ip_dict:
            self.ip_dict[identifying] = []

        attrib = (platform, app)
        self.ip_dict[identifying].append(attrib)

    def get_time(self, datetime):
        rexp = re.compile('\d+:\d+:\d+\s')
        m = rexp.search(datetime)
        if m:
            return m.group(0).replace(' ','')


def print_sort(dic, k='k', seq='assending'):
    if isinstance(dic, dict):
        i = {'k':0, 'v':1}
        sequence = {'assending': True, 'descending': False}
        l = sorted(dic.iteritems(), key=lambda d:d[i[k]], reverse = sequence[seq])
        print '{'
        for ele in l:
            print '\t' + str(ele[0]) + ': ' + str(ele[1])
        print '}'
    else:
        print dic

def print_behavior(behavior):

    for behave in behavior:
        print "\t\t" + "(" + behave[0] + ", " + behave[1] + ")"

if __name__ == '__main__':
    if not os.path.exists('dump/parsed'):
        p = LogParser('log/prod-freewheel.espn.go.com.full.log')
        p.proceed()
    else:
        p = cPickle.load(open('dump/parsed','rb'))


    proc = Processor(p)
    proc.reduce()
