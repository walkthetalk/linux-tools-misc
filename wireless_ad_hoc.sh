#!/bin/bash
set -e
ifconfig wlan0 down
iwconfig wlan0 mode ad-hoc
iwconfig wlan0 channel 3
iwconfig wlan0 essid 'nql-ah'
ifconfig wlan0 10.10.0.1 up

iptables -A FORWARD -i wlan0 -o eth0 -s 10.0.0.0/24 -m state --state NEW -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A POSTROUTING -t nat -j MASQUERADE
sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

