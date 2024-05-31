#!/bin/bash

data=$(date)
date
msg="Success-$date"
echo "$date"
token=$1
curl -X POST -H "Authorization: token $1"   -d "{ \"body\": \"$msg\" }"  "https://api.github.com/repos/mkpmanish/djangoapp/issues/$2/comments"
