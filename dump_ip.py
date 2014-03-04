#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  cPickle
from behavior import User
from sets import Set


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

    def dump(self):
        ips = Set()

        c = 0
        with open('dump/ip_sets', 'w') as ip_file:
            for user, behavior_list in self.behavior.iteritems():
                ip = user.IP
                if ip not in ips:
                    ips.add(ip)
                    ip_file.write(ip+'\n')
                    c += 1

        print 'ip totals ' + str(c)

if __name__ == '__main__':
    st = Statistician("")
    with open('dump/behavior_dict', 'rb') as dict_file:
        st = cPickle.load(dict_file)

    st.dump()
