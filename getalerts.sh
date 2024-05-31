#!/bin/bash

msg="$3-$RANDOM"
echo "$msg"
token=$1
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $token" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/mkpmanish/django_vulnerable_app/code-scanning/alerts

#curl -X POST -H "Authorization: token $1"   -d "{ \"body\": \"$msg\" }"  "https://api.github.com/repos/mkpmanish/djangoapp/issues/$2/comments"
