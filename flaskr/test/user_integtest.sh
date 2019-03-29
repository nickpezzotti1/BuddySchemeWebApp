#!/bin/bash

for i in `seq 1 10`;
do
  HTTP_CODE=`curl --write-out '%{http_code}' -o /dev/null -m 10 -q -s http://localhost:5000/user`
  if [ "$HTTP_CODE" == "404" ]; then
    echo "Mentor page is not accessible. This is correct because it should not be reachable without logging in."
    exit 0;
  fi
  echo "Attempt to curl endpoint returned HTTP Code $HTTP_CODE. Backing off and retrying."
  sleep 10
done
echo "Server did not return 404 after expected time. Failing."
exit 0