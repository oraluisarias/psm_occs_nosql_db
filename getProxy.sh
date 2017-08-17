#!/bin/bash

for proxy in $(cat /cloud/utils/bin/CloudBots/app/proxy.dat | sed '1d;s/  */ /g' | cut -d\  -f8);
do
		echo $proxy
		export http_proxy="http://${proxy}"
		export https_proxy="http://${proxy}"
        wget -T 8 -t 1 $1
		if [ $? -eq 0 ] ; then
			echo $proxy
			exit 0
		fi
done;

echo "No proxy could find this route..."	
exit 1