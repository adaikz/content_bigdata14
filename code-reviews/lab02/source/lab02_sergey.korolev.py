# base_creator.py

#!/opt/anaconda/envs/bd9/bin/python3
import happybase


def main():
    connection = happybase.Connection('bd-master.newprolab.com')
    try:
        connection.delete_table("sergey.korolev", disable=True)
    except:
        pass

    urls = {
        'UID': dict(),
        'URL': dict()
    }

    connection.create_table("sergey.korolev", urls)


if __name__ == "__main__":
    main()

# mapper.py

#!/opt/anaconda/envs/bd9/bin/python3
import sys


def main():
    for line in sys.stdin:
        line = line.split('\t')
        if len(line) == 3:
            UID, timestamp, URL = line
            if (UID != '-') & URL.startswith('http') & (timestamp != '-') & (timestamp != '') & (UID != ''):
                if int(UID) % 256 == 93:
                    print(UID + " \t" + URL.strip() + "\t" + timestamp)


if __name__ == "__main__":
    main()

# reducer.py

#!/opt/anaconda/envs/bd9/bin/python3
import happybase
import sys


def main():
    connection = happybase.Connection('bd-master.newprolab.com')
    table = connection.table("sergey.korolev")
    for line in sys.stdin:
        line = line.split('\t')
        if len(line) == 3:
            UID, URL, timestamp = line
            timestamp = int(float(timestamp) * 1000)
            table.put(UID, data={"data:url": URL.strip()}, timestamp=timestamp)


if __name__ == "__main__":
    main()

# run.sh

#!/usr/bin/env bash

'''
OUT_DIR="/user/sergey.korolev/lab02s"
NUM_REDUCERS=8

python3 base_creator.py

hadoop jar hadoop-streaming.jar \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files mapper.py,reducer_combiner.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input /labs/lab02data/facetz_2015_02_05 \
    -output ${OUT_DIR}.tmp > /dev/null
'''