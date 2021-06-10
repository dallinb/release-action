#!/bin/sh -e
env | cut -d= -f1 | sort
gitchangelog
ls
exit 0
