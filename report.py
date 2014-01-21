#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    report.py To generate the report.
'''

from stats import Statistician
import os

class Reporter:
    def __init__(self, data):
        self.data=data
    @staticmethod
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
    @staticmethod
    def print_behavior(behavior):

        for behave in behavior:
            timestamp=behave[0]
            if not isinstance(timestamp, basestring):
                timestamp=datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

            print "\t\t" + "(" + timestamp + ", " + behave[1] + ")"


    def overall(self):
        print 'Number of ads types is ' + str(len(self.data.stats['Ad']))
        for metric in self.data.stats:
            print metric+ ': '
            self.print_sort(self.data.stats[metric], 'v')
        print len(self.data.m3u8)
        for metric in self.data.quality:
            print metric+ ': '
            self.print_sort(self.data.quality[metric], 'k', 'descending')

    def behavior():
        for user in self.data.behavior:
            print user + ": "
            self.print_behavior(self.data.behavior[user])




if __name__ == '__main__':
    #if not os.path.exists('/dev/shm/cleaned.log'):
    #    os.system('bzcat /home/tangkai/DDQoE/dump/cleaned_log.bz2 > /dev/shm/cleaned.log')
    #st = Statistician('/dev/shm/cleaned.log')

    st = Statistician('/dev/shm/cleaned_run.log')
    st.gen_stats()
    reporter = Reporter(st)

    reporter.overall()
