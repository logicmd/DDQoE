f = open('/tmp/ram/d/prod-freewheel.espn.go.com.log')
d = {}
c = 0
for line in f:
    c+=1
    if len(d.get(line,[])) >= 1 and d[line][0] >= 1:
        d[line][0] += 1
        d[line].append(c)
    else:
        d[line] = []
        d[line].append(1)
        d[line].append(c)

for line, line_num_list in d.iteritems():
    if line_num_list[0] > 1:
        list_str = []
        for i in xrange(len(line_num_list)):
            if i>=1:
                list_str.append('#%d' %(line_num_list[i]))
                if i<len(line_num_list) - 1:
                    list_str.append(', ')
        print "Duplicate line(%d times) in %s detected:\n%s" %(line_num_list[0], ''.join(list_str), line)
