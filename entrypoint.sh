#!/bin/sh -e
env | cut -d= -f1 | sort
pwd
ls -al
echo "GITHUB_EVENT_NAME: ${GITHUB_EVENT_NAME}"
echo "GITHUB_REF: ${GITHUB_REF}"
gitchangelog
exit 0
