ps -ef|grep "itchat"|grep -v "grep"|awk '{print $2}'|xargs kill -9

