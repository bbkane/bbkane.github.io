+++
title = "Troubleshooting Connections"
date = 2017-01-30
updated = 2017-05-19
aliases = [ "2017/01/30/Troubleshooting-Connections.html" ]
+++

I recently had to set up a server with some legacy code that needed two
database connections that just wouldn't connect. This is how I troubleshooted
it

# Troubleshooting the first broken database connection

## Get a minimal example

The app connects to multiple databases. The first one
wouldn't connect through Apache, so I made a minimal example and ran it with
`PHP`.

```
php tmp.php
```

It still wouldn't but I googled the error and found that I had to replace the
`localhost` connection IP with `127.0.0.1`.

This worked! So the problem is with Apache running PHP, not PHP itself.

## Check Apache

I had a working copy of this code in a local VM, so I vimdiffed `phpinfo();`
from each. They looked the same except the one on the remote VM had a weird
IPV6 address.  I then checked Apache's logs (should have done this first) and
found that an IP address was set randomly because the hostname couldn't be
reliably determined. I used this to change a value in
`/etc/httpd/conf/httpd.conf`. I still don't know if that helped or not, but it
seemed like a good thing to do.

After that was done, though, my problem still wasn't over.

After googling the problem, I got to
[StackOverflow](http://stackoverflow.com/q/4078205/2958070). It looks like the
problem could be SELinux

## Check SELinux

I toggled the sebools mentioned in the answer:

```
setsebool -P httpd_can_network_connect=1
setsebool -P httpd_can_network_connect_db=1
```

and found [this
blog](https://major.io/2012/01/25/getting-started-with-selinux/) very useful to
see errors, make SELinux permissive (so it doesn't actually block anything) and
see more bools.

That worked! My database was connecting!

Unfortunately, the second database still wouldn't connect.

## Telnet

I then tried to make sure the connection worked between my VM and the database server.

```
nslookup <server_name> # works, so it's in DNS

ping <server_name> # still working
```

I tried to see if I could telnet to the port as well..

```
telnet <server_name> <port_name> # The default port for MSSQL
```

I could reach the port, but couldn't do anything... This was to be expected
because I didn't have any credentials. I just wanted to see if a firewall was
blocking the port.

## Capture packets

I could reach the port, so I didn't think it was the firewall. Maybe it was
still SELinux rolling through my processes, screwing my network up? The next
step was to capture some packets.

To capture the packet, I had to figure out what to capture.

I set up the code to first print it's PID, then try to connect to the database
in an infinite `while(true)` loop and found a command `ss` that let me see
socket information from a process.

The PHP code output looked something like this:

```
3974

Unable to connect...
Unable to connect...
...
```

Now that I had a PID and an attempt to use a socket, I traced the connection
with `ss`:

```
[root@ipplan-dev-local-tmp ~]# ss -tanp | grep 3974
ESTAB      0      0      <my_ip>:<my_port>              <db_server_ip>:<db_server_port>                users:(("php",pid=3974,fd=6))
```

So it looks like we have a connection from me on port `<my_port>` to the other
server on port `<db_server_port>`. That made sense, so why wasn't it doing
anything?

Time for some packet analysis.

```
tcpdump
```

That gave me an error that one interface (`nflog` I think) wasn't specified and
then it gave me a bunch of traffic.

I found the interface I needed with the `ip addr` command (on some systems
`ifconfig` shows the same thing). The interface was `en00033`

```
tcpdump -i en00033
```

Now I was getting some traffic. Time to filter it some more

```
tcpdump -i en00033 -S -c 1000 'host <db_server_ip>'
```

The `-S` option used absolute sequence numbers, and the `-c 1000` limited my
output to 1000 packets. `'host <db_server_ip>'` limited the packets captures to
being involved with my server.

That still worked, so I saved it to a file

```
tcpdump -i en00033 -S -c 1000 -w /tmp/dev.1.pcap 'host <db_server_ip>'
```

After running that for a little while, I `scp`'d the capture to my Mac for
analysis in WireShark and snagged my boss to help with the analysis.

```
# from my Mac:
scp <server_name>:/tmp/dev.1.pcap .

wireshark dev.1.pcap
```

Wireshark showed the application sending a SYN, the db returning a [SYN, ACK],
the app sending a SYN, a "Pre-TDS7 login", then that login being retransmitted
until the app finally sends a [FIN, ACK]. and restarts the sequence.  So we
have the standard 3-way handshake, then the db stops accepting anything else.
Very odd.

## Traceroute and firewall check

My boss still thought it might be the firewall and once we logged into the
firewall, we saw the dropped connections. Fixing that led to the application
working

## Capturing MySQL traffic for Analysis

Once verified that the application is working, it can sometimes be helpful to
see what SQL statements are actually generated by an application. In my
experience, this is best done by taking a packet capture and filtering out the
SQL with the following command modified from
[StackOverflow](http://stackoverflow.com/a/38171661/2958070):

```
tshark -r <name>.pcap -T fields -e mysql.query
```

Alternatively, you could capture the queries in real time by modifying the command slightly:

```
tshark -i <interface> -T fields -e mysql.query
```

Then analyze away!


