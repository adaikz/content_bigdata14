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
