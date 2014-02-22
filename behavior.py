#!/usr/bin/env python
# -*- coding: utf-8 -*-


ind2prog = {
        -3  : '_e_renderer-init',
        -2  : '_e_unknown',
        -1  : '_e_renderer-load',
         0  : 'defaultImpression',
         1  : 'firstQuartile',
         2  : 'midPoint',
         3  : 'thirdQuartile',
         4  : 'complete',
         5  : 'adEnd',
        10  : 'slotImpression',
        11  : 'slotEnd',
        }
prog2ind = {
        '_e_renderer-init'  : -3,
        '_e_unknown'        : -2,
        '_e_renderer-load'  : -1,
        'defaultImpression' : 0,
        'firstQuartile'     : 1,
        'midPoint'          : 2,
        'thirdQuartile'     : 3,
        'complete'          : 4,
        'adEnd'             : 5,
        'slotImpression'    : 10,
        'slotEnd'           : 11,
        }
class Behavior:
    def __init__(self):
        self.is_master = None
        self.is_ad = None
        self.is_media = None

class Master(Behavior):
    def __init__(self):
        self.is_master = True
    def __str__(self):
        return "master"
    #def strme(self):
    #    return self.__str__()

class Ad(Behavior):
    '''ind2prog = {
            0: 'defaultImpression',
            1: 'firstQuartile',
            2: 'midPoint',
            3: 'thirdQuartile',
            4: 'complete'
            }
    prog2ind = {
            'defaultImpression': 0,
            'firstQuartile': 1,
            'midPoint': 2,
            'thirdQuartile': 3,
            'complete': 4
            }'''
    def __init__(self, adid = None, progress = None):
        self.is_ad = True
        self.progress = prog2ind.get(progress, -10)
        self.ad_id = adid

    def __str__(self):
        return str(self.ad_id) + ', ' + ind2prog.get(self.progress, 'unknown')

    #def strme(self):
    #    return self.__str__()

class Media(Behavior):
    def __init__(self, bitrate = None):
        self.is_media = True
        self.bitrate = bitrate

    def __str__(self):
        return str(self.bitrate) + 'kbps'

    #def strme(self):
    #    return self.__str__()

class User():
    def __init__(self, IP = None, platform = None, app = None):
        self.IP = IP
        self.platform = platform
        self.app = app
    def __str__(self):
        return str(self.IP) + ", " + str(self.platform) + ", " + str(self.app)

    def __hash__(self):
        return hash((self.IP, self.platform, self.app))
    def __eq__(self, other):
        return (self.IP, self.platform, self.app) == (other.IP, other.platform, other.app)

class Feature():
    def __init__(self, device=None, bitrate=None, switchoff=None, st_time=None, time_len=None, ad_percentage=None):
        self.device = device
        self.bitrate = bitrate
        self.switchoff = switchoff
        self.st_time = st_time
        self.time_len = time_len
        self.ad_percentage = ad_percentage

    def __str__(self):
        return "%s, %d kbps, %d times, at %.2f, %.1f secs, %.4f" %(self.device, self.bitrate, self.switchoff, self.st_time,
                self.time_len, self.ad_percentage)

