#!/bin/sh -e
env | cut -d= -f1 | sort
pwd
ls -al
gitchangelog
exit 0
