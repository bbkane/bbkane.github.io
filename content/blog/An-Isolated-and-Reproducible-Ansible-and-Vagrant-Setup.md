+++
title = "An Isolated and Reproducible Ansible and Vagrant Setup on Mac"
date = 2017-10-27
updated = 2021-02-08
aliases = [ "2017/10/27/An-Isolated-and-Reproducible-Ansible-and-Vagrant-Setup.html" ]
+++

Ansible is a great tool for automating system maintenance. This is how I install it. My notes differ from the official ones in the following ways:

- I install as much of this software as I can isolated from the system tools.
  This means I can update my projects and the system code independently and I
  can uninstall my tools cleanly.
- I've added notes for integrating VM creation with Vagrant/VirtualBox and
  Ansible. This trio really works nicely when you want to spin up a VM or
  network of VMs, do horrible dangerous things to them, and finally kill them
  when you mess up too badly. All of this information is stored in relatively
  portable files, so it's easy to make a base configuration for VMs then
  customize it for different projects.

## Install Ansible

Ansible does not support Windows. These notes are specifically for Mac, though
they *should* be trivial to modify for Linux.  [The Ansible
docs](http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-on-mac-osx)
suggests that we should use pip to install it. This means that we need to
install Python to use its pip. Macs have an older version of python, so I like
to install a new one with Anaconda. This has two purposes- it gets me a modern
and easily uninstallable version of Python, and it will let me isolate my
Ansible install from the rest of the system, making it easier to install
multiple versions of Ansible and also uninstall it.

## Install Anaconda Python

I use the 3.6 64-bit Command-Line Installer

- [Download link](https://www.anaconda.com/download/#download)
- [Install Instructions](https://docs.anaconda.com/anaconda/install/mac-os#macos-graphical-install)
  (scroll to command line part)

You want to install it to the default location and prepend the install location
to the PATH

Follow any notes at the end of the install.

```
If this is your first install of dbus, automatically load on login with:
    mkdir -p ~/Library/LaunchAgents
    cp /Users/bkane/anaconda3/org.freedesktop.dbus-session.plist ~/Library/LaunchAgents/
    launchctl load -w ~/Library/LaunchAgents/org.freedesktop.dbus-session.plist
```

Anaconda Python includes a lot more than what you need for Ansible (for
example, type `jupyter qtconsole` to get a nice Python CLI).

## Create an environment for Ansible

We could install Ansible globally, but we'll want to update and test different
versions against each other.  To that end, we'll make a separate environment
for the current version of ansible.

- First make a folder:

```bash
mkdir -p ~/Code/Python/ansible-2.4
cd !$
conda create --name ansible-2.4 python=3
```

## Enter the environment

```bash
source activate ansible-2.4
```

You should see your prompt change and if you type `which python`, you'll see
this environment has its own copy of Python.

## Install `ansible`

```bash
pip install ansible==2.4
```

Test it:

```bash
ansible --version
```

## Save the environment

Let's save the environment to a file.  This will let you give this file another
Mac user and they'll be able to reproduce your Ansible install.  Very helpful
for debugging.

```bash
conda env export -f environment.yaml
```

## Exit the environment

When you're done playing with Ansible, type `source deactivate` to exit the environment.

Ansible is now installed. To actually play with it though, we can use the
vagrant and VirtualBox tools to launch Linux VMs for us to experiment with
and then kill when we screw them up too badly.

## Install Virtualbox

- I currently use [Virtualbox 5.2.2](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

## Install Vagrant

- I currently use [vagrant 2.0.2](https://releases.hashicorp.com/vagrant/2.0.2/)

## Launch a small VM network

At this point, we've installed all the programs we need to. The rest of this is creating the right files and running commands. 

```bash
mkdir -p ~/Code/Vagrant/small_network
cd !$
```

We'll be staying in this folder for all further commands and file creation.

Copy the following into a text file called
`~/Code/Vagrant/small_network/Vagrantfile`. If you don't have a text editor
installed to do this, I recommend [Visual Studio
Code](https://code.visualstudio.com/).

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure('2') do |config|
  # set settings common to all VMs
  config.vm.box = 'centos/7'
  # Disable the default synced folder because it's too much trouble to set up
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.synced_folder '.', '/home/vagrant/sync', disabled: true

  # Don't check the host key
  config.ssh.verify_host_key = false

  # Add some VirtualBox specific settings
  config.vm.provider 'virtualbox' do |vb|
    vb.gui = true
    vb.customize ['modifyvm', :id, '--clipboard', 'bidirectional']
  end

  # Create and set VM specific settings
  config.vm.define :node1 do |node1|
    node1.vm.hostname = 'node1'
  end

  config.vm.define :node2 do |node2|
    node2.vm.hostname = 'node2'
  end
end
```

Feel free to read the
[docs](https://www.vagrantup.com/intro/getting-started/index.html), but we're
really just using Vagrant to give us easily buildable and destroyable VMs.

With the Vagrantfile in place, we've built a small network of two nodes. Let's turn it on:

```bash
cd ~/Code/Vagrant/small_network
vagrant up
```

Test by SSHing into the two nodes:

```
vagrant ssh node1
exit  # exit from inside the VM
vagrant ssh node2
exit  # exit from inside the VM
```

## Use Ansible with our VMs

### Create a `hosts.ini` for Ansible

We need to tell Ansible about our VMs and how to connect to them. Copy the
following into `~/Code/Vagrant/small_network/hosts.ini`:

```
node1
node2
```

### Tell Ansible to use Vagrant's SSH settings

If we tried to connect to `node1` and `node2` as-is from Ansible, Ansible won't be able to find them. To fix this we need to export Vagrant's SSH settings to an SSH config file and tell Ansible to use that file.

```
vagrant ssh-config > ssh_config
```

Next we need to connect that `ssh_config` to Ansible with an `ansible.cfg` file in the `small_network` directory. In this file, I've also enabled some other useful options.
See [the docs](http://docs.ansible.com/ansible/latest/intro_configuration.html) for more info:

```ini
[defaults]
host_key_checking = False
retry_files_enabled = False
inventory = hosts.ini
# This presents a window for a logged-in attacker,
# but it's a small window and I need what it enables
# See http://docs.ansible.com/ansible/latest/become.html#becoming-an-unprivileged-user
allow_world_readable_tmpfiles = True

# https://stackoverflow.com/a/45086602/2958070
stdout_callback=debug
stderr_callback=debug

[ssh_connection]
# generate ssh_config with `vagrant ssh-config`
ssh_args = -F ./ssh_config
```

And test it  (make sure you are in `~/Code/Vagrant/small_network/` and are
using your ansible environment (`source activate ansible-2.4`)):

```bash
ansible all -m ping
```

You should get something like the following:

```javascript
(ansible-2.4) ✔ ~/Code/Vagrant/small_network
15:09 $ ansible -i hosts.yaml all -m ping
node1 | SUCCESS => {
    "changed": false,
    "failed": false,
    "ping": "pong"
}
node2 | SUCCESS => {
    "changed": false,
    "failed": false,
    "ping": "pong"
}
```

## Manipulate the VMs

To turn off the VMs, type `vagrant halt`. To turn them back on again, type `vagrant up`

## Further Steps

At this point we've installed Anaconda Python, Ansible (in it's own isolated
environment), Virtualbox, and vagrant. We've taught Ansible how to find and
login to the VMs we've spun up, and we're ready to start really learning
Ansible. Head to the [Getting
Started](http://docs.ansible.com/ansible/latest/intro_getting_started.html) and
follow it. We've already done about the first 3rd, but we integrated Vagrant
instead of modifying the global `/etc/ansible/hosts` file. The (See also) links
at the bottom of the page are your next steps. Enjoy!

## Uninstalling all of this

Eventually, you might stop working with Ansible, or find a way you like more,
and you might want to uninstall everything or parts of this stack. Here's how,
starting from the VMs down

### Erase a VM

```bash
cd ~/Code/Vagrant/small_network/
vagrant destroy
```

Optionally delete `~/Code/Vagrant/small_network` if you're absolutely sure you
won't want to recreate your work.

### Uninstall Vagrant

Follow the [Uninstallation Page](https://www.vagrantup.com/docs/installation/uninstallation.html)

### Uninstall Virtualbox

Follow [this
guide](https://osxuninstaller.com/uninstall-guides/properly-uninstall-virtualbox-mac-solved/).
It basically recommends that you quit the app and run the uninstallation
script.

### Remove the virtual environmant

Run `conda remove --name ansible-2.4 --all`

Optionally delete `~/Code/Python/ansible-2.4` if you'll never need the environment again.

### Remove Anaconda Python

Follow [this StackOverflow link](https://stackoverflow.com/a/42182997/2958070)
and remove the `PATH` manipulation in your `~/.bashrc` or `~/.bash_profile`.
