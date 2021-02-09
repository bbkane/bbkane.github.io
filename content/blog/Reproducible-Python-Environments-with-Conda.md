+++
title = "Reproducible Python Environments with Conda"
date = 2017-05-17
updated = 2017-10-20
aliases = [ "2017/05/17/Reproducible-Python-Environments-with-Conda.html" ]
+++

By default, Python doesn't handle binary dependencies very well.  There have
been several occasions when I've tried to `pip install library` and it just
choked on me because it was trying to compile something and I didn't have the
magic combination of compiler versions and build tools needed. At the same
time, it's absolutely worth fiddling with many of these libraries because they
can be tremendously powerful. Matplotlib, Paramiko, and Neovim are Python
libraries I depend on that have binary dependencies. Luckily, this hard problem
has been alleviated by [conda](https://conda.io/docs/intro.html), a "package,
dependency and environment manager for any language". It isn't perfect, but it
lives up to the name and also solves a related problem: creating lightweight,
cross-platform, easily-reproducible environments for Python code. Here's an example of
how I use conda with my code, including common problems I run into and how I
solve them. The [docs](https://conda.io/docs/get-started.html) have been very
helpful.

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
that. I'm going to call it remote-uptime, and I know from experience that a
script like that needs a library named [paramiko](http://www.paramiko.org/) to
run and paramiko needs an binary crytography implementation (which makes it
difficult to install via pip).  Furthermore I want to use the
[netmiko](https://github.com/ktbyers/netmiko) wrapper on top of paramiko so I
can also use this for network devices. So those are my goals, create an
environment with paramiko and netmiko, then save those dependencies so the
environment can be easily reproduced elsewhere.

## Create Environment and install libraries

First things first- find out out which libraries are in conda's repos, and
which will have to be installed via pip. The output of `conda search paramiko`
indicates that that it is in conda's repos. That's really good because it means
that we can let conda deal with paramiko's binary dependencies. However, `conda
search netmiko` comes up empty, so the next step is to search for any binary
dependencies it has, and try to deal with those independently of the
environment. I normally deal with this situation by probing the website for
installation instructions, and linking those in the README for my project.
However, in this case, netmiko's dependencies are pure Python except for
paramiko, which is already being dealt with by conda. Finally, let's actually
create the darn thing:

```
conda create --name multi-uptime python=3 paramiko
```

This command creates an environment with a completely separate copy of Python
and some libraries for us.

Notice I'm only specifying the libraries that conda can install in the command
above- We'll deal with the ones that need pip... right after we activate the
environment.

```
source activate multi-uptime
```

This command makes sure that the `multi-uptime` version of Python is the first
one found on our PATH- this means that whenever we do any more python things
with this (like installing netmiko), it will only affect this copy of Python,
leaving our system installation of Python unentangled with the copy dedicated to
multi-uptime. The prompt also changes to tell us we're using a project specific
Python version.

```
21:36:29 [bbkane@bbkane-Latitude-E7440 Code]
$ source activate multi-uptime
(multi-uptime) 21:36:39 [bbkane@bbkane-Latitude-E7440 Code]
$
```

Now let's install netmiko:

```
python -m pip install netmiko
```

You'll notice that it does install some helper libraries, but the binary
dependent one is already installed:

```
Requirement already satisfied: paramiko>=1.13.0 in /home/bbkane/anaconda3/envs/multi-uptime/lib/python3.6/site-packages (from netmiko)
```

So conda has helped us successfully sidestep netmiko's binary dependencies
without having to install packages at the system level!

The last step on our setup now is to save this mix of libraries to a text file
so other contributors can use it without going through the same dance we've had
to:

```
conda env export > environment.yaml
```

`environment.yaml` looks like this:

```
name: multi-uptime
channels:
- defaults
dependencies:
- asn1crypto=0.22.0=py36_0
- cffi=1.10.0=py36_0
- cryptography=1.8.1=py36_0
- idna=2.5=py36_0
- libffi=3.2.1=1
- openssl=1.0.2l=0
- packaging=16.8=py36_0
- paramiko=2.1.2=py36_0
- pip=9.0.1=py36_1
- pyasn1=0.2.3=py36_0
- pycparser=2.18=py36_0
- pyparsing=2.2.0=py36_0
- python=3.6.2=0
- readline=6.2=2
- setuptools=27.2.0=py36_0
- six=1.10.0=py36_0
- sqlite=3.13.0=0
- tk=8.5.18=0
- wheel=0.29.0=py36_0
- xz=5.2.2=1
- zlib=1.2.8=3
- pip:
  - netmiko==1.4.2
  - pyyaml==3.12
  - scp==0.10.2
prefix: /home/bbkane/anaconda3/envs/multi-uptime
```

Notice that dependencies is a list of items- mostly Python libraries, but also
other things, like Python itself, binary libraries, like OpenSSL, and pip, which
has its own list of libraries. This is basically a superset of what `pip freeze`
gives. The last thing to note is that last line there- `prefix: /path/to/env`.
To be honest, I'm not sure why that line is there. It doesn't need to be, and
keeping actually hampers using this environment.yaml on another machine. Delete
it (so in this example, `- scp==0.10.2` would be the last line), and save this
file in your repository.

## Use it on another machine

When someone else wants to use your environment, they only have to use the
following command:

```
conda env create -f environment.yaml
```

Which will do all the work we just did without them having to do much of
anything.

## Delete the environment

When you need more space, or you screw something up and you want to delete the environment, use

```
conda remove --name <name> --all
```

Because `conda` stores environments separately from your code, you don't have to worry about it deleting anything you created, and if you need it the environment back, you can just recreate it with your `environment.yaml`.
