# Базу создаем в консоли
create 'evgeny.permyakov', {NAME => 'data', VERSIONS => 4096}


# Запускаем map-only задачу

#!/opt/anaconda/envs/bd9/bin/python
import happybase
import sys

def main():
    for line in sys.stdin:

        try:
            uid, time, url = line.strip().split('\t')
        except:
            continue

        # UID и timestamp числа
        try:
            float(uid)
            float(time)
        except:
            continue

        # uid из моего варианта 34
        if (float(uid) % 256) == 34: pass
        else: continue

        # uid целое и timestamp - дробь
        if float(uid).is_integer() and not float(time).is_integer(): pass
        else: continue


        # Url начинается с https
        if url.startswith('http'):pass
        else: continue

        connection = happybase.Connection('bd-node2.newprolab.com')
        table = connection.table('evgeny.permyakov')
        table.put(uid.encode(), {b'data:url': url.encode()}, timestamp=int(float(time) * 1000))

if __name__ == '__main__':
    main()
