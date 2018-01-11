---
layout: default
title: Fixing HTTPS CA Cert Issues
---

Disclaimer: I'm very new to understanding SSL, and I haven't yet put in the
effort to be authoritative about this subject. This post describes how to work
with a modified chain of trust from a VM without the last certificate installed.

Websites (and HTTPS requests in general) use a system called SSL Certificates to
verify that a URL visited is actually being served the legitimate provider for
it (as opposed to someone hiding between your computer and the provider and
capturing your data). They also encrypt your data so no one else can read it. SSL
Certificates are usually installed on the Operating System by the vendor (as far
as I know), but they can be updated and new ones can be installed. On Linux,
this is usually the `ca-certificates` package.

## How Firewalls intercept secure traffic

In a corporate environment, the security department never likes the fact
that encrypted information can be passed between employees and outside
websites. The way I understand this, they intercept requests going out
(usually at the firewall level) decrypt them, inspect them for naughtiness, then
re-encrypt them and complete the request. When the answering request comes from
the website, the firewall does the same thing. Here is a diagram:

### Parties Involved:

- `Client` (think desktop user)
- `FW` (firewall at the edge of the corporate network)
- `Site` (google.com, facebook.com or any other site the Client is visiting) (this
  could also be an API)

### Non-inspected Flow:

1. `Client` creates encrypted request with the CA Cert pre-installed for `Site` and sends it
  to `Site`
1. `Site` decrypts it with its own certificate, creates a response, encrypts it,
  and sends it back
1. `Client` decrypts the response.

### Inspected Flow:

In the inspected flow, the client is pre-installed with a "universal"
certificate and the firewall is installed with the coordinating certificate. It
uses this cert to decrypt the request, does it's thing, then encrypts it with
the certificate for the website.

1. `Client` creates encrypted request with the CA Cert pre-installed for `FW` and
  sends it to `Site`
1. `FW` intercepts request, decrypts it with its coordinating certificate,
  inspects it, re-encrypts it with the certificate for `Site`, and sends it to
  `Site`
1. `Site` decrypts it with its own certificate, creates a response, encrypts it,
  and sends it back
1. `FW` intercepts request, decrypts it with its coordinating certificate,
  inspects it, re-encrypts with it's certificate, and sends it to `Client`
1. `Client` decrypts the response.

If you study these flow, you'll notice that this is pretty much transparent to
`Client`. `Client` doesn't have to do anything special to get it's traffic
inspected.

## The Problem with VMs

However, this becomes a problem if, in the development process, you make a
request from a VM hosted on your machine (a sub-client of `Client`, kinda). In
this case, the firewall intercepts the request and can't decrypt it because it
wasn't encrypted with the firewall's certificate.

To fix this, you can either disable certificate checking (which means you can't
be reasonably sure you aren't going to a fake website- very bad) or you can add
the `Client`'s 'firewall certificate to the VM's store of them. This post is
really about how to find that certificate, put it on the VM, and use it in your
code (specifically Python's `requests` library).

## Find the Certificate (on a Mac) (with FireFox and Keychain Access)

To find the certificate, open Firefox and go to a website that supports HTTPS
(for example [Google](https://www.google.com/)), and click the green lock in the
URL bar.

![]({{ site.baseurl }}/img/2018-01-11-Fixing-HTTPS-CA-Cert-Issues/url_bar.png)

Use the buttons to export the certificate:

1. the arrow on the right side of the lock popup
1. "More Information"
1. "View Certificate" (in the Security Tab)
1. Switch tabs to Details in the Certificate Viewer
1. Export...

Save it somewhere you can find again with a nice descriptive name.

If you open the certificate in a text editor, you'll see something like the
following:

```
-----BEGIN CERTIFICATE-----
awScGmdnsbolcfUlYCvZRMFHwcTIcEuEzmahqBoKWqCPHYoLucnDfuKgoYqiLKDC
XJHFHBkInJfshLLgyCDXypjDDlgHHpYJvquWoBNTypJCWNWIwxWZCVbdoDiJBbAg
... more lines
-----END CERTIFICATE-----
```

## Push the certificate

Of course, you can simply `scp` the certificate:

`scp path/to/cert.crt vagrant@vm_ip:path/to/cert.crt`

Or, if you're using Ansible to manage the VM, you can use the `copy` module to
put it on:


```yaml
- name: Push CA Certs to VM
copy:
  force: false  # Don't overwrite a file already there
  src: path/to/cert.crt
  dest: path/to/cert.crt
```

## Use the Certificate

I place the certificate at the user level (under `~`), but I'm fairly certain
you can add it at the system level by placing it in `/etc/ssl/certs`. I haven't
tested this theory.

In the
[`requests`](http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification)
library, you can point to your certificate with the `verify`
keyword parameter:

```python
import requests
response = requests.get('https://www.google.com', verify='path/to/cert.crt')
```

And then, of course, you can do whatever you want with the output.

So, that's how I deal with certificates in VMs.
