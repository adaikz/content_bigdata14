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
