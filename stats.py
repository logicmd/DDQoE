#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bz2, os, re, datetime

'''
    stats.py refactor the processor logics
'''

class Statistician:
    def __init__(self, file):
        self.file = file
        self.stats = {
            'Platform': {},
            'App': {},
            'Ad': {},
            'Progress': {}
        }

        self.m3u8 = []

        self.quality = {
            'ad': {},
            'content': {}
        }

        self.behavior = {}
        self.ip_dict = {}

    def gen_stats(self):
        if 'bz2' in self.file:
            f = bz2.BZ2File(self.file, 'r')
        else:
            f = open(self.file, 'r')
        for line in f:
            elements = line.split(', ')
            self.reduce(elements)

        for user in self.behavior.keys():
            self.behavior[user].sort(key=lambda x:x[0], reverse=False) # Time

    def reduce(self, elements):
        platform_stats = self.stats['Platform']
        platform = elements[3]
        platform_stats[platform] = platform_stats.get(platform, 0) + 1

        app_stats = self.stats['App']
        app = elements[4].replace('\n','')
        app_stats[app] = app_stats.get(app, 0) + 1

        ad = self.stats['Ad']
        progress = self.stats['Progress']

        req = elements[2]
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

        time = float(elements[1])
        IP = elements[0]
        self.update_behavior(
                IP,
                platform,
                app,
                time,
                behave
             )

        #self.update_ip_dict( IP, platform, app )


    def get_quality(self, url):

        br = None

        if 'K/' in url:
            rexp=re.compile('/\d+K/')
            match=rexp.search(url)
            if match:
                br = int(match.group(0).replace('/','').replace('K',''))
                bitrate = br #str(br) + 'kbps'
                self.quality['ad'][bitrate] = self.quality['ad'].get(bitrate, 0) + 1


        elif 'ads' in url:
            if 'master' in url:
                br = 'master'
                self.quality['master'] = self.quality.get('master', 0) + 1
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
        identifying = ip + '-' + app
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
        timestamp=behave[0]
        if not isinstance(timestamp, basestring):
            timestamp=datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

        print "\t\t" + "(" + timestamp + ", " + behave[1] + ")"

if __name__ == '__main__':
    if not os.path.exists('dump/cleaned_log.bz2'):
        c = Cleaner('log/prod-freewheel.espn.go.com.full.log','./dump/cleaned_log.bz2')
        c.proceed()


    st = Statistician('dump/cleaned_log.bz2')


    # url = "http://espnlive-akc.bamnetworks.espn.go.com/ls04/espn/2013/12/21/ESPN_VIDEO_5S_M3U8_1378283_20131221/400K/400_slide.m3u8"
    # print st.get_quality(url)



    st.gen_stats()

    # Stats
    print 'Number of ads types is ' + str(len(st.stats['Ad']))
    for metric in st.stats:
        print metric+ ': '
        print_sort(st.stats[metric], 'v')
    print len(st.m3u8)
    for metric in st.quality:
        print metric+ ': '
        print_sort(st.quality[metric], 'k', 'descending')

    # behavior
    for user in st.behavior:
        print user + ": "
        print_behavior(st.behavior[user])

