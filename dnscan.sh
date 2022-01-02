#!/bin/bash

echo "
██████╗ ███╗   ██╗███████╗
██╔══██╗████╗  ██║██╔════╝
██║  ██║██╔██╗ ██║███████╗
██║  ██║██║╚██╗██║╚════██║
██████╔╝██║ ╚████║███████║
╚═════╝ ╚═╝  ╚═══╝╚══════╝
    https://github.com/m3x/
    ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ███████╗██║     ███████║██╔██╗ ██║
    ╚════██║██║     ██╔══██║██║╚██╗██║
    ███████║╚██████╗██║  ██║██║ ╚████║
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝"

mode=$1

if [ "$mode" = "-sb" ]
then
	p_mode="B-F Sub domain"

elif [ "$mode" = "-st" ]
then
	p_mode="Sub domain TakeOver"

elif [ "$mode" = "-zt" ]
then
	p_mode="Transfer Zone"

else

        echo " "
        echo "     -sb   Sub domain bruteforce"
        echo "     -st   Sub domain takeover"
        echo "     -zt   Zone transfer testing"
        echo " "
        echo " Run > sh $0 <mode> (for usage help)"
        echo " "
        exit
fi


if [ "$mode" = "-sb" ] || [ "$mode" = "-st" ] || [ "$mode" = "-zt" ]
then

	domain=$2
	list=$3

	if [ "$mode" = "-zt" ] && [ "$domain" = "" ]; then echo "Use: sh $0 $mode <your.domain>"; exit; fi

	if [ "$list" = "" ] && [ "$mode" = "-zt" ]
	then
		ip=$(host $domain | grep "has address" | cut -d " " -f 4 | head -n 1)
		echo " "
		if [ "$ip" = "" ]; then echo "Sorry, host [ $domain ] not found"; exit; fi
		echo "[$p_mode]"
		echo "[$domain] [$ip]"
		echo " "
		echo "-----------------------------"
		echo " "

	        for i in $(host -t ns $domain | cut -d " " -f 4)
	        do
	                host -l -a $domain $i

	        done

		exit
	fi

	tuto="Use: sh $0 $mode <your.domain> <wordlist>"

	if [ "$2" = "" ]
	then
		echo $tuto
		echo " "
		exit

	elif [ "$3" = "" ]
	then
		echo $tuto
		echo " "
		exit
	fi

        ip=$(host $domain | grep "has address" | cut -d " " -f 4 | head -n 1)
	echo " "
	if [ "$ip" = "" ]; then echo "Sorry, host [ $domain ] not found"; exit; fi
        echo "[$p_mode]"
        echo "[$domain] [$ip]"
        echo " "
	echo "-----------------------------"
	echo " "

	for subdomain in $(cat $list)

	do
		if [ "$mode" = "-sb" ];then
	        	host $subdomain.$domain | grep -v "NXDOMAIN"

		elif [ "$mode" = "-st" ];then
			host -t CNAME $subdomain.$domain | egrep "is an alias"

		fi
	done


fi
