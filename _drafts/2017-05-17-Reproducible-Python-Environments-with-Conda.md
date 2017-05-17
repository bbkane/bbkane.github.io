---
layout: default
title: Reproducible Python Environments with Conda
---

By default, Python doesn't handle binary dependencies very well.  There have been
several occasions when I've tried to `pip install library` and it just choked on
me because it was trying to compile something and I didn't have the magic
combination
of compiler versions and build tools needed. At the same time, it's absolutely
worth fiddling with many of these libraries because they can be tremendously
powerful. Matplotlib, Paramiko, and Neovim are Python libraries I depend on that
have binary dependencies. Luckily, this hard problem has been alleviated by
[conda](https://conda.io/docs/intro.html), a "package, dependency and
environment manager for any language". It isn't perfect, but it lives up to the
name and also solves a related problem: creating lightweight, cross-platform,
easily-reproducible environments for code. Here's an example of how I use conda
with my code, including common problems I run into and how I solve them.

## Install [miniconda3](https://conda.io/docs/install/quick.html#linux-miniconda-install).

I usually do this on Linux, so I'm only going to put those instructions here.
Follow the link above to find instructions for other platforms.

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Follow the instructions, and make sure you prepend Miniconda's directory to the
PATH when it gives you the option, then start a new terminal instance.

## Create a new project

I like to create my project in it's own directory with a README.md to explain
what it does. This is usually the point when I decide what libraries I'm going
to need for this code. For the sake of this blog post, let's say I want to write
a script that SSHes into a Linux box, runs the command `uptime`, and prints
that. I know from experience that a script like that needs a library named
[paramiko](http://www.paramiko.org/) to run and paramiko needs an binary
crytography implementation (which makes it difficult to install via pip). Furthermore I want to use the
[netmiko](https://github.com/ktbyers/netmiko) wrapper on top of paramiko so I
can also use this for network devices.

## Create Environment and install libraries

TODO:
- demonstrate installing paramiko with pip
- finish this blog post...
