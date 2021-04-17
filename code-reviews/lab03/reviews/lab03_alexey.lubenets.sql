create database alexey_lubenets;

use alexey_lubenets;

# натягиваем мету на сырой вход
CREATE EXTERNAL TABLE IF NOT EXISTS alexey_lubenets
    (uid string, action_dt string, url string)
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION '/user/alexey.lubenets/lab03data/'
;

# удаляем и создаем вьюшку для реализации требуемой бизнес-логики
DROP VIEW alexey_lubenets.lab03;

CREATE VIEW alexey_lubenets.lab03 as
    with get_data as (
            select uid, replace(replace(replace(replace(url, '%3A', ':'), '%2F', '/'), 'http://', ''), 'https://', '') as url_
                    , url as url_old
                from alexey_lubenets.alexey_lubenets
                where uid is not null and lower(trim(uid)) != ''
        ), clean_data as (
            select uid, replace(substr(url_, 1, instr(url_, '/')-1), 'www.', '') as url
                from get_data
        ), categorize_data as (
            select uid
                    , sum(case when url='cars.ru'               then 1 else 0 end) as user_cat11
                    , sum(case when url='avto-russia.ru'        then 1 else 0 end) as user_cat12
                    , sum(case when url='bmwclub.ru'            then 1 else 0 end) as user_cat13

                    , sum(case when url='postnauka.ru'          then 1 else 0 end) as user_cat21
                    , sum(case when url='plantarium.ru'         then 1 else 0 end) as user_cat22
                    , sum(case when url='lensart.ru'            then 1 else 0 end) as user_cat23

                    , sum(case when url='pass.rzd.ru'           then 1 else 0 end) as user_cat31
                    , sum(case when url='rzd.ru'                then 1 else 0 end) as user_cat32
                    , sum(case when url='vokrug.tv'             then 1 else 0 end) as user_cat33

                    , sum(case when url='apteka.ru'             then 1 else 0 end) as user_cat41
                    , sum(case when url='doctor.ufacity.info'   then 1 else 0 end) as user_cat42
                    , sum(case when url='womanhit.ru'           then 1 else 0 end) as user_cat43
                from clean_data
                group by uid
        )
        select uid
                , case when user_cat11>=10 or user_cat12>=10 or user_cat13>=10
                        then 1 else 0 end as user_cat1_flag
                , case when user_cat21>=10 or user_cat22>=10 or user_cat23>=10
                        then 1 else 0 end as user_cat2_flag
                , case when user_cat31>=10 or user_cat32>=10 or user_cat33>=10
                        then 1 else 0 end as user_cat3_flag
                , case when user_cat41>=10 or user_cat42>=10 or user_cat43>=10
                        then 1 else 0 end as user_cat4_flag
            from categorize_data
;

# сохраняем результаты из вьюшки в файле на hdfs
INSERT OVERWRITE DIRECTORY 'hdfs://bd-master.newprolab.com:8020/user/alexey.lubenets/lab03result'
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    select * from alexey_lubenets.lab03
;
