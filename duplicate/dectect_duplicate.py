f = open('/tmp/ram/d/prod-freewheel.espn.go.com.log')
d = {}
c = 0
for line in f:
    c+=1
    d[line] = d.get(line, 0) + 1
    if d[line] > 1:
        print "Duplicate line in #" + str(c) + " detected:\n" + line
