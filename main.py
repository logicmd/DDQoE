#!/usr/bin/env python
#-*- coding: utf-8 -*-
import cPickle, os
from log_parser import LogParser
from processor import Processor

def log_parser_pro():
    p=LogParser('log/prod-freewheel.espn.go.com.log.bz2', 5)
    p.proceed()
    if not len(p.datetime) == len(p.request) == len(p.UA) == len(p.platform) == len(p.app):
        raise IndexError('Sample Number Not Consistent')
    f=open('/tmp/ram/parsed','w')
    cPickle.dump(p, f, True)
    f.close()

def integration():

    if not os.path.exists('dump/parsed'):
        p = LogParser('log/prod-freewheel.espn.go.com.full.log')
        p.proceed()
    else:
        p = cPickle.load(open('dump/parsed','rb'))


    proc = Processor(p)
    proc.reduce()

    # Stats
    # print 'Number of ads types is ' + str(len(proc.stats['Ad']))
    # for metric in proc.stats:
    #     print metric+ ': '
    #     print_sort(proc.stats[metric], 'v')
    # print len(proc.m3u8)
    # for metric in proc.quality:
    #     print metric+ ': '
    #     print_sort(proc.quality[metric], 'k', 'descending')

    # behavior
    # for user in proc.behavior:
    #     print user + ": "
    #     for behave in proc.behavior[user]:
    #         print "\t\t" + "(" + str(behave[0]) + ", " + str(behave[1]) + ")"

    # ip_stats
    for ip in proc.ip_dict:
        print ip + ": "
        for attrib in proc.ip_dict[ip]:
            print "\t\t" + "(" + str(attrib[0]) + ", " + str(attrib[1]) + ")"

    #for u in proc.m3u8:
    #    print u
    #for url in proc.m3u8:
    #    print url


if __name__ == '__main__':
    log_parser_pro()
