#!/usr/bin/env python
# извелечение требуемого из входного набора
import sys

for line in sys.stdin:
    elements = line.split("\t")
    try:
        if len(elements) == 3 and elements[0].strip() not in '-' and (elements[2].strip()).startswith('http'):
            (UID, timestamp, URL) = elements
            if int(UID) % 256 == 10:
                print(line)
    except Exception:
        continue

#!/opt/anaconda/envs/bd9/bin/python
# coding=utf8

# сохранение в hbase-базу
import happybase
import sys

table_name = 'alexey.lubenets'

c = happybase.Connection(host='bd-master.newprolab.com')
c.open()

print(c.tables())
try:
    c.disable_table(table_name)
    c.delete_table(table_name)
except Exception:
    print(Exception)

c.create_table(table_name, {'data': dict(max_versions=4096)})
table = c.table(table_name)
print(table)

for line in sys.stdin:
    print(line)
    items = line.split("\t")
    if len(items) == 3:
        (UID, ts, URL) = items
        timestamp = int(float(ts) * 1000)
        # print(timestamp)
        table.put(UID, {'data:url': URL.strip()}, timestamp=timestamp)
        print(line + ' is saved')

# проверка сохраненного
for uid in ['3331220746', '3281840906']:
    pairs = table.cells(uid, 'data:url', versions=30, timestamp=None, include_timestamp=True)
    print(pairs)

for key, data in table.scan():
    print(str(key) + ': ' + str(data))