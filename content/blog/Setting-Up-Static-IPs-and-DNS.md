+++
title = "Setting Up Static IPs and DNS"
date = 2018-10-09
updated = 2018-10-09
aliases = [ "2018/10/09/Setting-Up-Static-IPs-and-DNS.html" ]
+++

I want machines on my network to be able to talk to each other via hostnames
(fqdns). Here's how I set that up.

## Router

On my [local router](http://tplinkwifi.net) (a TP-Link Archer C3150), I set up static
IPs for each device. The right menu is located from

*Advanced* Tab at the top -> *Network* button to the left -> *DHCP Server* beneath *Network*

Static IPs must be in the local LAN (192.168.0.1/24 for me from the *Network* ->
*LAN* menu) and I prefer them not to be in the DHCP pool either
(192.168.0.100-200). So I gave my devices some static IPs starting from
192.168.0.201. This does limit me to 54 devices.

I had to reset the router before pinging the static IPs would work.

## Registrar

Next is setting up DNS entries on my Registrar. I use [NameCheap](namecheap.com)
and finding the menu for this wasn't too hard:

*Manage* To the left of the selected domain -> *Advanced DNS* at the top -> *Add
New Record*

I added an `A : lin01.bbkane.com -> 192.168.0.203` record with an auto TTL
(which for some reason is 1701 right now...).

At this point, I'm able to ping a host by the new fully qualified domain name.

NOTE: because these fqdns are publicly available, they present security risks:

- Someone could see what devices I have by inspecting DNS
- I could connect to the wrong host while connected to someone else's private
  network.

For my use case, both of these risks are acceptable.

## Device

This part [isn't strictly necessary](https://serverfault.com/a/228111), but it
is nice.

### [Mac](https://apple.stackexchange.com/a/287775/249419)

For some reason, one of these commands failed...

```
➜  ~  sudo scutil --set LocalHostName mac01.bbkane.com.local
SCPreferencesSetLocalHostName() failed: Invalid argument
```

### [Linux](https://www.cyberciti.biz/faq/linux-change-hostname/)

```
$ hostnamectl set-hostname lin01.bbkane.com
$ systemctl reboot
```
