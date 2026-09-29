#!/bin/bash

show_hello() {
	echo "Hello!"
}

show_hostname() {
	host=$(hostname)
	echo "Hostname: $host"
}

show_disk() {
	disk=$(df -h /)
	echo "Disk: $disk"
}

show_memory() {
	memory=$(free -h)
	echo "Memory: $memory"
}

show_uptime() {
	uptime=$(uptime)
	echo "Uptime: $uptime"
}

show_users() {
	users=$(users)
	echo "Users: $users"
}

show_help() {
	echo "Usage:"
	echo "./server-tool.sh hello"
	echo "./server-tool.sh host"
	echo "./server-tool.sh disk"
	echo "./server-tool.sh memory"
	echo "./server-tool.sh help"
	echo "./server-tool.sh uptime"
	echo "./server-tool.sh users"
}

case "$1" in
	hello)
		show_hello
		;;
	disk)
		show_disk
		;;
	hostname)
		show_hostname
		;;
	memory)
		show_memory
		;;
	help)
		show_help
		;;
	uptime)
		show_uptime
		;;
	users)
		show_users
		;;
	*)
		echo "Unknown command. Use 'help' for more info"
		exit 1
		;;
esac


