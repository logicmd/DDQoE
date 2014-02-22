#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from cleanup import Cleaner
from stats import Statistician

'''
    run.py
'''


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
    if not os.path.exists('/dev/shm/in.log'):
        os.system('bzcat /home/tangkai/DDQoE/log/prod-freewheel.espn.go.com.log.bz2 >' +
                '/dev/shm/in.log')
    if True or not os.path.exists('/dev/shm/cleaned_run.log'):
        c = Cleaner(input = '/dev/shm/in.log', output = '/dev/shm/cleaned_run.log', continued = 13339588948)
        c.proceed()


    st = Statistician('/dev/shm/cleaned_run.log')


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

