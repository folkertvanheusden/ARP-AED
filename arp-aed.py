#! /usr/bin/python3

# MAC / IP address usage, by folkert@vanheusden.com
# MIT license

import ipaddress
import os
import socket
import sys


device = sys.argv[1]
user = sys.argv[2]


def str_to_mac(s):
    return b''.join([int(e, 16).to_bytes(1) for e in s.split(':')])


ignore_list = set([str_to_mac(e) for e in sys.argv[3:]])
ignore_list.add(str_to_mac('ff:ff:ff:ff:ff:ff'))  # ignore broadcast


def mac_to_str(m):
    return ':'.join([f'{b:02x}' for b in m])


def ip4_to_str(i):
    return str(ipaddress.IPv4Address(i))


def ip6_to_str(i):
    return str(ipaddress.IPv6Address(i))


s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
s.bind((device, 0))

os.setuid(int(user))

macs = { }
ip4s = { }
ip6s = { }


def remember(macs, mac_from, ips, ip_from):
    # count ip4s per mac
    if not mac_from in macs:
        macs[mac_from] = set()
    if not ip_from in macs[mac_from]:
        macs[mac_from].add(ip_from)
        if len(macs[mac_from]) > 1:
            print(f'{mac_to_str(mac_from)} has multiple IP addresses: {", ".join(macs[mac_from])}')

    # count macs per ip4
    if not ip_from in ips:
        ips[ip_from] = set()
    if not mac_from in ips[ip_from]:
        ips[ip_from].add(mac_from)
        if len(ips[ip_from]) > 1:
            print(f'{ip_from} has multiple MACs: {", ".join(ips[ip_from])}')


while True:
    raw_packet, addr = s.recvfrom(65535)

    if raw_packet[12] == 0x08 and raw_packet[13] == 0x00:  # IP4
        mac_from = raw_packet[6:12]
        if mac_from in ignore_list:
            continue

        ip4_from = ip4_to_str(raw_packet[14 + 12: 14 + 12 + 4])
        remember(macs, mac_from, ip4s, ip4_from)

    if raw_packet[12] == 0x86 and raw_packet[13] == 0xdd:  # IP6
        mac_from = raw_packet[6:12]
        if mac_from in ignore_list:
            continue

        ip6_from = ip6_to_str(raw_packet[14 + 8: 14 + 8 + 16])
        remember(macs, mac_from, ip6s, ip6_from)
