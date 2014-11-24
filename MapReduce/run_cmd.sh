#!/bin/bash

#
HADOOP_USER_NAME=hduser hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-*streaming*.jar -D mapred.job.reduces=0 -files mapper_only.py -mapper mapper_only.py -input /user/hduser/bealstreasure/* -output /user/hduser/bealstreasure-output-`date +%s` 

#-reduce NONE

#HADOOP_USER_NAME=hduser hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-*streaming*.jar -file mapper.py -mapper mapper.py -file reducer.py -reducer reducer.py -input /user/hduser/bealstreasure/* -output /user/hduser/bealstreasure-output-`date +%s`
