#'21/Dec/2013:21:08:43' does not match format 'dd/MMM/YYYY:HH:mm:ss'
import datetime

print datetime.datetime.strptime('21/Dec/2013:21:08:43', '%d/%b/%Y:%H:%M:%S')

print datetime.datetime.fromtimestamp(1384972547.0).strftime('%H:%M:%S')

print isinstance(1384972547.0, basestring)

print "a, b, c".split(', ')

l=[1,3,2,4]
ll=[]
for i in xrange(len(l)):
    if i>0:
        ll.append('#%d' %l[i])
        if i<len(l)-1:
            ll.append(', ')

print ll

f = open('./ml/data/test', 'w')
f.write('fuck\n')
