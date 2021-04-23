#!/usr/bin/env bash

# alexey.lubenets: 2021_04_22: думаю, что для решения данной лабы достаточно использования только маппера.
# замечаний к оформлению нет, код понятный и структурированный => комментарии и не требуются

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