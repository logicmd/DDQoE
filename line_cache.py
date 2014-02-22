import cPickle
# Read in the file once and build a list of line offsets

c = 23788265

f = open('/dev/shm/in.log', 'r')
line_offset = []
offset = 0
i = 0
for line in f:
    i += 1
    line_offset.append(offset)
    offset += len(line)
    if i > c + 10:
        break

#cPickle.dump(line_offset, open('./dump/src_line_cache', 'w'), True)
print line_offset[c]
