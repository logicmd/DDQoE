import urllib2
import json
import time
import io
import sys
import cPickle
import atexit

ip_dict = {}
dump_file = './dump/ip'

def dump():
    with open(dump_file, 'w') as f:
        cPickle.dump(ip_dict, f, True)

atexit.register(dump)

class IPHelper:
    def __init__(self):
        self.load_plain()
        self.load()

    def load_plain(self):
        global ip_dict
        with open('./report/ip_with_time_zone') as f:
            for line in f:
                l = line.split(' ')
                ip_dict[l[0]] = int(l[1])

        with open('./report/ips.txt') as f:
            for line in f:
                l = line.split(' ')
                ip_dict[l[0]] = int(l[1])

    def load(self):
        global ip_dict, dump_file
        try:
            with open(dump_file, 'r') as f:
                ip_dict = cPickle.load(f)
                f.close()
        except:
            print "Warning: no exsited ip dump file"

    def get_time_zone(self, ip, retry=10):
        global ip_dict
        time_zone = None

        if retry <= 0:
            print "maximum retry reached, set %s to -6\n" %(ip)
            time_zone = -6

        elif ip not in ip_dict or ip_dict[ip] is None:
            try:
                time.sleep(0.5)
                req = urllib2.Request(
                       'http://api.ipinfodb.com/v3/ip-city/' +
                        '?key=076b47ff1eefd89fde7cfc1409d808f48949e1eb0f2eb08e66786358d207e81d' +
                        '&ip='+ ip +'&format=json'
                        )
                response = urllib2.urlopen(req)
                page = json.load(response)
                time_zone = int(page["timeZone"][:3])
                with open('./report/ips.txt', 'a') as ff:
                    ff.write("%s %d" %(ip, time_zone))
                ip_dict[ip] = time_zone
            except ValueError as e:
                print "unable to resolve IP: %s, set to -6\n%s" %(ip, e)
                time_zone = -6
            except Exception as e:
                print "IP: %s failed\n%s" %(ip, e)
                print "retrying, sleep 5s..."
                time.sleep(5)
                self.get_time_zone(ip, retry-1)
        else:
            time_zone = ip_dict[ip]

        if time_zone is None:
            time_zone = -6

        return time_zone

def offline():
    ip_helper = IPHelper()
    with open("./dump/ip_sets", 'r') as f:
        for line in f:
            ip = line.strip('\n')
            time_zone = ip_helper.get_time_zone(ip)
            print "%s %d" %(ip, time_zone)

if __name__ == "__main__":
    ip_helper = IPHelper()
    print ip_helper.get_time_zone("216.190.59.146")
    print ip_helper.get_time_zone("63.247.1.254")

