#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Request:
    def __init__(self, IP=None, datetime=None, size=None, UA=None):
        self.IP=IP
        self.datetime=datetime
        self.size=size
        self.UA=UA


if __name__ == '__main__':
    r = Request('1.2.3','1233/1232','1231','abc')
    print r.IP

