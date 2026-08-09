## ARP-AED

This program lists which MAC addresses have multiple IP4/6 addresses or vice versa.

## Usage

sudo ./arp-aed.py eth0 1000 ...

* eth0 is the Ethernet adapter to listen on
* 1000 is the user ID to change to after opening the Ethernet device (e.g. your own user id)
* ... can be 0 or more MAC addresses to ignore


## who & license

Written by Folkert van Heusden <folkert@vanheusden.com>

Released under MIT license
