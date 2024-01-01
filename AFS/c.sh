#!/bin/bash

while true; do
    ps aux | grep 'python3 new.d.py' | grep -v 'bash -c' | awk '{print $2}' | xargs -r kill
    sleep 600
done