## ARP-AED

This program lists which MAC addresses have multiple IP4/6 addresses or vice versa.

## Usage

Run `./arp-aed.py -h` to see a list of options.

Example:
```bash
sudo ./arp-aed.py -d eth0 -u 1000 -l -x 00:16:3e:cd:89:d2
```

* eth0 is the Ethernet adapter to listen on
* 1000 is the user ID to change to after opening the Ethernet device (e.g. your own user id)
* -l prevents it from listing link local IP6 addresses
* -x makes it ignore the 00:16:3e:cd:89:d2 MAC address (your gateway for example)


## who & license

Written by Folkert van Heusden <folkert@vanheusden.com>

Released under MIT license
