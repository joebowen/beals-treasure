#!/bin/bash

HADOOP_USER_NAME=hduser hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-*streaming*.jar -file mapper.py    -mapper mapper.py -file reducer.py   -reducer reducer.py -input /user/hduser/gutenberg/* -output /user/hduser/gutenberg-output-`date +%s`
