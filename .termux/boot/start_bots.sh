#!/bin/bash
termux-wake-lock
sleep 10
pkill -9 -f python
cd /data/data/com.termux/files/home
nohup python bot_alert.py > alert.log 2>&1 &
nohup python bot_amazon.py > amazon.log 2>&1 &
nohup python bot_iscritti.py > iscritti.log 2>&1 &
