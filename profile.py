#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bz2, os, re, datetime, cPickle
import urllib2, json, time

from behavior import Master, Ad, Media, User, Feature
from ipinfo import IPHelper
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


        self.quality = {
            'ad': {},
            'content': {}
        }

        self.behavior = {}
        self.feature_file = './ml/data/feature.csv'
        self.time_train_file = './ml/data/time_train'
        self.ad_train_file = './ml/data/ad_train'

    def gen_stats(self):
        if 'bz2' in self.file:
            f = bz2.BZ2File(self.file, 'r')
        else:
            f = open(self.file, 'r')
        for line in f:
            elements = line.split(', ')
            self.organize(elements)

        for user in self.behavior.keys():
            self.behavior[user].sort(key=lambda x:x[0], reverse=False) # Time


    def organize(self, elements):
        if len(elements) < 5:
            return
        platform_stats = self.stats['Platform']
        platform = elements[3]
        platform_stats[platform] = platform_stats.get(platform, 0) + 1

        app_stats = self.stats['App']
        app = elements[4].replace('\n','')
        app_stats[app] = app_stats.get(app, 0) + 1

        ad = self.stats['Ad']
        progress = self.stats['Progress']

        req = elements[2]

        behave = None

        raw_id = self.get_quartile(req, 'adid');
        raw_progress = self.get_quartile(req, 'cn');

        if raw_id and raw_progress:
            adid = int(raw_id);
            ad[adid] = ad.get(adid, 0) + 1;

            prog = raw_progress;
            progress[prog] = progress.get(prog, 0) + 1;

            behave = Ad(int(raw_id), raw_progress)

            if behave.progress < -5:
                raise NameError("Unrecognized ad pingback progress: \n" + raw_progress)

        else:
            raw_m3u8_url = self.get_quartile(req, '_fw_lpu')
            if raw_m3u8_url:
                m3u8_url = raw_m3u8_url.replace('%3A',':')
                bitrate = self.get_quality(m3u8_url)
                if bitrate == 'master':
                    behave = Master()
                else:
                    behave = Media(bitrate)


        time = float(elements[1])
        IP = elements[0]

        u = User(IP, platform)
        self.update_behavior( u, time, behave )

    def reduce(self, interval=300):

        ip_helper = IPHelper()

        feature_output = open(self.feature_file, 'w')
        time_train_4 = open(self.time_train_file+'4', 'w')
        ad_train_4 = open(self.ad_train_file+'4', 'w')

        time_train_2 = open(self.time_train_file+'2', 'w')
        ad_train_2 = open(self.ad_train_file+'2', 'w')

        time_train_3_plat = open(self.time_train_file+'3_plat', 'w')
        ad_train_3_plat = open(self.ad_train_file+'3_plat', 'w')

        time_train_3_init_ts = open(self.time_train_file+'3_init_ts', 'w')
        ad_train_3_init_ts = open(self.ad_train_file+'3_init_ts', 'w')

        #summary = open('./ml/data/summary', 'w')

        platform2ind = \
        {
            'Apple TV': 1,
            'Mac': 2,
            'Windows': 3,
            'iPad': 4,
            'Android': 5,
            'iPhone': 6,
            'iPod' : 7,
            'None' :8,
        }

        media_num = 0
        ad_num = 0
        master_num = 0

        for user, behavior_list in self.behavior.iteritems():
            previous_ts = 0
            initial_ts = 0

            bitrate_list = []
            switchoff = 0
            #time_len = 0
            ad_prog_dict = {}


            for i in xrange(len(behavior_list)):

                ts = behavior_list[i][0]
                if initial_ts == 0:
                    initial_ts = ts
                behave = behavior_list[i][1]

                if isinstance(behave, Ad):
                    prog = behave.progress
                    ad_prog_dict[prog] = ad_prog_dict.get(prog, 0) + 1
                    #print prog, ad_prog_dict[prog]
                    ad_num += 1

                elif isinstance(behave, Media):
                    bitrate = behave.bitrate
                    if len(bitrate_list) > 0 and not bitrate == bitrate_list[-1]:
                        switchoff += 1

                    bitrate_list.append(behave.bitrate)
                    media_num += 1

                elif isinstance(behave, Master):
                    master_num += 1

                if i == len(behavior_list) - 1:

                    avg_bitrate = -1
                    if len(bitrate_list) > 0:
                        avg_bitrate = sum(bitrate_list) * 1.0 / len(bitrate_list)
                        time_len = behavior_list[i][0] - initial_ts


                    ad_percentage = -1.00
                    wired = False
                    if ad_prog_dict.get(0, 0) != 0:
                        ad_cal = {}
                        for ad_prog in xrange(4):
                            k = 0.25 * ad_prog
                            ad_cal[k] = ad_prog_dict.get(ad_prog, 0) - ad_prog_dict.get(ad_prog + 1, 0)
                            if ad_cal[k] <= -1:
                                wired = True
                        ad_cal[1.00] = ad_prog_dict.get(4, 0)
                        ad_percentage = 0.00
                        for percentage, count in ad_cal.iteritems():
                            ad_percentage += percentage * count;
                        ad_percentage /= ad_prog_dict[0]
                        #ad_percentage = (\
                        #    0.00 * (ad_prog_dict.get(0, 0) - ad_prog_dict.get(1, 0)) + \
                        #    0.25 * (ad_prog_dict.get(1, 0) - ad_prog_dict.get(2, 0)) + \
                        #    0.50 * (ad_prog_dict.get(2, 0) - ad_prog_dict.get(3, 0)) + \
                        #    0.75 * (ad_prog_dict.get(3, 0) - ad_prog_dict.get(4, 0)) + \
                        #    1.00 * ad_prog_dict.get(4, 0) ) / ad_prog_dict.get(0, 0)
                        if wired or ad_percentage > 1 or ad_percentage < 0:
                            print "******************wired**********************"
                            print "user: %s\n behavior:" %(user)
                            for b_tuple in behavior_list:
                                print '\t' + str(b_tuple[1])
                            print "[0.00]: %d, [0.25]: %d, [0.50]: %d, [0.75]: %d, [1.00]:%d" \
                                    %(ad_prog_dict.get(0, -1), ad_prog_dict.get(1, -1), \
                                      ad_prog_dict.get(2, -1), ad_prog_dict.get(3, -1), \
                                      ad_prog_dict.get(4, -1))

                    timezone_offset = ip_helper.get_time_zone(user.IP)
                    #timezone_offset = -6
                    initial_ts = \
                        int(datetime.datetime.fromtimestamp(initial_ts + timezone_offset * 60 * \
                            60).strftime('%H')) + \
                        int(datetime.datetime.fromtimestamp(initial_ts).strftime('%M')) * 1.0 / 60
                    f = Feature(user.platform, avg_bitrate, switchoff, initial_ts,
                            time_len, ad_percentage)
                    #print f

                    feature_output.write('%.1f,%.4f,%.1f,%d,%d,%.2f,%d\n' \
                            %(time_len, ad_percentage, avg_bitrate, switchoff, \
                            platform2ind[user.platform], initial_ts, len(bitrate_list)))

                    if time_len > 0 and avg_bitrate >= 0 and not wired \
                            and ad_percentage >= 0 and ad_percentage <= 1:

                        switchoff = switchoff * 1.0 / ( time_len ) * 60.0
                        time_train_4.write('%.1f 1:%.1f 2:%.2f 3:%d 4:%.2f\n' %(time_len, avg_bitrate,
                            switchoff, platform2ind[user.platform], initial_ts))

                        ad_train_4.write('%.2f 1:%.1f 2:%.2f 3:%d 4:%.2f\n' %(ad_percentage, avg_bitrate,
                            switchoff, platform2ind[user.platform], initial_ts))

                        time_train_3_plat.write('%.1f 1:%.1f 2:%.2f 3:%d\n' %(time_len, avg_bitrate,
                            switchoff, platform2ind[user.platform]))

                        ad_train_3_plat.write('%.2f 1:%.1f 2:%.2f 3:%d\n' %(ad_percentage, avg_bitrate,
                            switchoff, platform2ind[user.platform]))

                        time_train_3_init_ts.write('%.1f 1:%.1f 2:%.2f 3:%.2f\n' %(time_len, avg_bitrate,
                            switchoff, initial_ts))

                        ad_train_3_init_ts.write('%.2f 1:%.1f 2:%.2f 3:%.2f\n' %(ad_percentage, avg_bitrate,
                            switchoff, initial_ts))

                        time_train_2.write('%.1f 1:%.1f 2:%.2f\n' %(time_len, avg_bitrate, switchoff))

                        ad_train_2.write('%.2f 1:%.1f 2:%.2f\n' %(ad_percentage, avg_bitrate, switchoff))

                        #ip_file.write('%s %d\n' %(user.IP, timezone_offset))
                        #summary.write('ad: %d, media: %d, master: %d\n' %(ad_num, media_num, master_num))

                    bitrate_list[:] = []
                    switchoff = 0
                    ad_prog_dict.clear()

                    initial_ts = ts

                previous_ts = ts

        feature_output.close()
        time_train_2.close()
        ad_train_2.close()
        time_train_3_plat.close()
        ad_train_3_plat.close()
        time_train_3_init_ts.close()
        ad_train_3_init_ts.close()
        time_train_4.close()
        ad_train_4.close()

        print "Ad num %d\nMedia num: %d\nMaster num: %d\n" %(ad_num, media_num, master_num)

    def get_quality(self, url):

        br = None

        if 'K/' in url:
            rexp=re.compile('/\d+K/')
            match=rexp.search(url)
            if match:
                br = int(match.group(0).replace('/','').replace('K',''))
                bitrate = br #str(br) + 'kbps'
                self.quality['ad'][bitrate] = self.quality['ad'].get(bitrate, 0) + 1

        elif 'K.m3u8' in url:
            rexp=re.compile('\d+K.m3u8')
            match=rexp.search(url)
            if match:
                br = int(match.group(0).replace('K.m3u8',''))
                bitrate = br #str(br) + 'kbps'
                self.quality['content'][bitrate] = self.quality['content'].get(bitrate, 0) + 1

        elif 'adhoc' in url or ('ads' in url and 'master' in url):
                br = 'master'
                self.quality['master'] = self.quality.get('master', 0) + 1

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

            elif 'tablet' in url or 'mobile' in url or 'console' in url:
                br = 'master'
                self.quality['master'] = self.quality.get('master', 0) + 1
            else:
                self.quality['unknown'] = self.quality.get('unknown', 0) + 1
                raise NameError('unable to parse the bitrate in the url:\n' + url)

        else:
            self.quality['unknown'] = self.quality.get('unknown', 0) + 1
            raise NameError('unable to parse the bitrate in the url:\n' + url)

        return br


    def get_quartile(self, text, tagname):
        st_ind = text.find('&' + tagname + '=')
        en_ind = text[st_ind+len(tagname):].find('&')
        if st_ind>-1:
            if en_ind>-1:
                return text[st_ind+len(tagname)+2:st_ind+len(tagname)+en_ind]
            else:
                return text[st_ind+len(tagname)+2:]


    def update_behavior(self, user, time, behave):
        if user not in self.behavior:
            self.behavior[user] = []

        behavior = (time, behave)
        self.behavior[user].append(behavior)


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
    #if not os.path.exists('dump/cleaned_log.bz2'):
    #    c = Cleaner('log/prod-freewheel.espn.go.com.full.log','./dump/cleaned_log.bz2')
    #    c.proceed()

    force_refresh = False

    #st = Statistician('dump/cleaned_log.bz2')
    st = Statistician('/dev/shm/cleaned.log')

    dict_file = 'dump/behavior_dict'
    if force_refresh or not os.path.exists(dict_file):
        st.gen_stats()
        cPickle.dump(st, open(dict_file, 'wb'), True)
    else:
        st = cPickle.load(open(dict_file, 'rb'))

    st.reduce()

    # Stats
    print 'Number of ads types is ' + str(len(st.stats['Ad']))
    for metric in st.stats:
        print metric+ ': '
        print_sort(st.stats[metric], 'v')

    for metric in st.quality:
        print metric+ ': '
        print_sort(st.quality[metric], 'k', 'descending')

    # behavior
    #for user in st.behavior:
    #    print str(user) + ": "
    #    print_behavior(st.behavior[user])

