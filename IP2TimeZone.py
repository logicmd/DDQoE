import urllib2
import json
import time
import io
import sys

d = {}

def getTimeZone(IP):
    global d
    time_zone = None
    if IP not in d:
        req = urllib2.Request(
            'http://api.ipinfodb.com/v3/ip-city/' +
            '?key=076b47ff1eefd89fde7cfc1409d808f48949e1eb0f2eb08e66786358d207e81d' +
            '&ip=' + IP + '&format=json')
        response = urllib2.urlopen(req)
        the_page = json.load(response)
        time_zone = int(the_page["timeZone"][:3])
        d[IP] = time_zone
    else:
        time_zone = d[IP]

    return "%s %d" %(IP, time_zone)

if __name__ == "__main__":
    ifile = open('./dump/ip_sets', 'r')
    ofile = open('./dump/ip_with_time_zone', 'w')
    efile = open('./report/err', 'w')
    for line in ifile:
        ip = line.strip('\n')
        try:
            o = getTimeZone(ip)
            print o
            ofile.write(o + '\n')
        except Exception, e:
            print "*************"
            print ip + " failed"
            print "*************"
            efile.write(ip + '\n')
        time.sleep(0.5)

    ifile.close()
    ofile.close()
    efile.close()
