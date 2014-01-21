#!/bin/sh
mount -o remount,size=61G /dev/shm
#mount -o size=60G -o nr_inodes=1000000 -o noatime,nodiratime -o remount /dev/shm
