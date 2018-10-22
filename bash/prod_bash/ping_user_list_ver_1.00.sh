#!/bin/bash
# Program name: ping_user_list_ver_1.00.sh
echo "Bash script to ping user list you enter."
echo "Enter filename: "
read VAR_FILENAME
date
cat $VAR_FILENAME |  while read output
do
    ping -c 1 "$output" > /dev/null
    if [ $? -eq 0 ]; then
    echo "node $output is up"
    else
    echo "node $output is down"
    fi
done
