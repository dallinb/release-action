#!/bin/sh -e
echo "GITHUB_EVENT_NAME: ${GITHUB_EVENT_NAME}"
echo "GITHUB_REF: ${GITHUB_REF}"
gitchangelog > CHANGELOG.md
changed_files=$( git status -s )

if [ $changed_files -ne '0' ]; then
  echo 'The CHANGELOG.md is out of date.'
  exit 1
fi

exit 0
