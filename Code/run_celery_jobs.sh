#!/bin/bash

#lsof -i :6379
#kill -9 <process_id>
redis-server ./server/conf/redis.conf &> ./server/logs/redis.log &
#redis-server 

chmod +x celery_worker.sh
chmod +x celery_beat.sh

open -a Terminal.app ./celery_worker.sh
open -a Terminal.app ./celery_beat.sh
