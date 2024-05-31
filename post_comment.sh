#!/bin/bash
date=${date}
body = "Successfull - $date"
curl -X POST -H "Authorization: token $1" -d {"body":$body} 'https://api.github.com/repos/mkpmanish/djangoapp/issues/40/comments'
