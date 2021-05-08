"""Лаба 2. Загрузить данные в HBase из большого лог-файла, лежащего в HDFS с помощью MapReduce"""

# 1.Подключение к HBASE через happybase

import happybase

#Создание подключения
connection = happybase.Connection('bd-master.newprolab.com')

#Создание таблицы
connection.create_table(
    'name.surname',
    {'data:url': dict(max_versions=4096)
    }
)

# 2.Код маппера (весь функционал реализован в нем, без редьюсера)

#!/usr/bin/python
import sys
import happybase

def main(): #Mapper
    for ext_line, line in enumerate(sys.stdin):
        map(None, line)

def map(external_key, line):
    try:
        uid, timestamp, url = line.strip().split('\t')
        #Убираем некорректные строки
        if (uid == '-') | (timestamp == '-') | (url == '-'):
            pass
        #Проверка, что uid число и условие из варианта
        elif (int(uid) % 256 != 154) | (uid.isdigit()==False): 
            pass
        #Проверка, что url начинается с http 
        elif (url[:4] != 'http'):
            pass
        else:            
            connection = happybase.Connection('bd-master.newprolab.com')
            connection.table('name.surname').put(uid.encode(), {b'data:url': url.encode()}, timestamp=int(float(timestamp)*1000)
    except:
        pass

if __name__ == '__main__':
    main()

# 3.Запуск jar-файла через терминал
hadoop jar /usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming.jar -D mapred.reduce.tasks=1\
    -files /data/home/name.surname/lab_2/lab2/mapper.py\
    -input /labs/lab02data/facetz_2015_02_12\
    -output /user/name.surname/lab2/result\
    -mapper mapper.py
