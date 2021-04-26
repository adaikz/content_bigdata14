## Шаг 1. Обработка доменов

Сначала запустим map-only задачу чтобы выделить и классифицировать домены

```python
#!/opt/anaconda/envs/bd9/bin/python
import sys
from urllib.parse import urlparse, unquote
import re

def url2domain(url):
   try:
       a = urlparse(unquote(url.strip()))
       if (a.scheme in ['http','https']):
           b = re.search("(?:www\.)?(.*)",a.netloc).group(1)
           if b is not None:
               return str(b).strip()
           else:
               return ''
       else:
           return ''
   except:
       return

# Списки доменов для категорий
cat1_lst = [u'cars.ru', u'avto-russia.ru', u'bmwclub.ru']
cat2_lst = [u'samara-papa.ru', u'vodvore.net', u'mama51.ru']
cat3_lst = [u'sp.krasmama.ru', u'forum.krasmama.ru', u'forum.omskmama.ru']
cat4_lst = [u'novayagazeta.ru', u'echo.msk.ru', u'inosmi.ru']

def main():
    for line in sys.stdin:

        try: 
            uid, time, url = line.strip().split('\t')
        except:
            continue

        # Выделим домен из ссылки
        domain = url2domain(url)
        
        if domain in cat1_lst:
            category ='cat1'
        elif domain in cat2_lst:
            category ='cat2'
        elif domain in cat3_lst:
            category ='cat3'
        elif domain in cat4_lst:
            category ='cat4'
        else:
            category ='no_cat'
        
        print(f"{uid}\t{domain}\t{category}")
    
if __name__ == '__main__':
    main()
```



## Шаг 2. Создадим таблицу в Hive

И загрузим туда результаты MR

```sql
create external table lab03
(
    uid BIGINT,
    domain string,
    category string
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
stored as textfile
location '/user/evgeny.permyakov/hive_data/lab03';


LOAD DATA INPATH '/user/evgeny.permyakov/part-00000' INTO TABLE lab03;
```

## Шаг 3. Основное решение

* Через WITH реализуем логику отесения человека к группе
* Через цепочу **left join** формируем таблицу в требуемом формате

```sql
WITH T1 AS (
SELECT 
	uid,
	category ,
	`domain` ,
	COUNT(*) 
FROM 
	lab03
GROUp BY
	uid ,
	category ,
	`domain` 
HAVING 
	COUNT(*) >= 10
)

INSERT OVERWRITE DIRECTORY 'hdfs://bd-master.newprolab.com:8020/user/evgeny.permyakov/lab03result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
SELECT 
	aa.uid,
	NVL(bb.flag_cat1, 0),
	NVL(cc.flag_cat2, 0),
	NVL(dd.flag_cat3, 0),
	NVL(ee.flag_cat4, 0)
FROM (SELECT DISTINCT uid FROM lab03 ) aa
LEFT JOIN (SELECT DISTINCT uid, 1 as flag_cat1  FROM T1 WHERE category = 'cat1') bb
	ON aa.uid = bb.uid 
LEFT JOIN (SELECT DISTINCT uid, 1 as flag_cat2  FROM T1 WHERE category = 'cat2') cc
	ON aa.uid = cc.uid 
LEFT JOIN (SELECT DISTINCT uid, 1 as flag_cat3  FROM T1 WHERE category = 'cat3') dd
	ON aa.uid = dd.uid 
LEFT JOIN (SELECT DISTINCT uid, 1 as flag_cat4  FROM T1 WHERE category = 'cat4') ee
	ON aa.uid = ee.uid 
ORDER BY
    aa.uid ASC
```

