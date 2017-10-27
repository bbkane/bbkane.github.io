# An Isolated and Reproducible Ansible and Vagrant Setup

Ansible does not support Windows. This was set up using a Mac.

http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-on-mac-osx

suggests that we should use pip to install it. This means that we need to
install Python to use its pip. Macs have an older version of python, so I like
to install a new one with Anaconda. This has two purposes- it gets me a modern
and easily uninstallable version of Python, and it will let me isolate my
Ansible install from the rest of the system, making it easier to install
multiple versions of Ansible and uninstall it.

## Install Anaconda Python

I use the 3.6 64-bit Command-Line Installer

- https://www.anaconda.com/download/#download
- https://docs.anaconda.com/anaconda/install/mac-os#macos-graphical-install
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
pip install ansible
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

- I use [Virtuabox 5.1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

## Install Vagrant

- I use [vagrant 1.8.7](https://releases.hashicorp.com/vagrant/1.8.7/)

## Launch a small VM network

```bash
mkdir -p ~/Code/Vagrant/small_network
cd !$
```

Copy the following into a file called `~/Code/Vagrant/small_network/Vagrantfile`

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure('2') do |config|
  config.vm.box = 'centos/7'
  # Disable the default synced folder because it's too much trouble to set up
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.synced_folder '.', '/home/vagrant/sync', disabled: true

  config.vm.provider 'virtualbox' do |vb|
    vb.gui = true
    vb.customize ['modifyvm', :id, '--clipboard', 'bidirectional']
  end

  config.vm.define :node1 do |node1|
    node1.vm.network :private_network, ip: '10.0.0.11'
    node1.vm.hostname = 'node1'
    :q

  end

  config.vm.define :node2 do |node2|
    node2.vm.network :private_network, ip: '10.0.0.12'
    node2.vm.hostname = 'node2'
  end
end
```

Feel free to read the
[docs](https://www.vagrantup.com/intro/getting-started/index.html), but we're
really just using Vagrant to give us easily buildable and destroyable VMs.

Test by SSHing into the first node:

```
ssh vagrant@10.0.0.11  # password: vagrant
```

You'll have to accept the key fingerprint, but then you should be in.
Log into the next one (`10.0.0.12`) and accept the key fingerprint as well.

This puts our public SSH key in the `~/.ssh/authorized_keys` on those systems-
we'll need that for Ansible to reach it.

## Use Ansible with our VMs

We need to tell Ansible about our VMs and how to connect to them. Copy the
following into `~/Code/Vagrant/small_network/hosts.yaml`:

```yaml
all:
  hosts:
    node1:
      ansible_host: 10.0.0.11
      ansible_ssh_user: vagrant
      ansible_ssh_private_key_file: ~/Code/Vagrant/small_network/.vagrant/machines/node1/virtualbox/private_key
    node2:
      ansible_host: 10.0.0.12
      ansible_ssh_user: vagrant
      ansible_ssh_private_key_file: ~/Code/Vagrant/small_network/.vagrant/machines/node2/virtualbox/private_key
```

And test it  (make sure you are in `~/Code/Vagrant/small_network/` and are
using your ansible environment (`source activate ansible-2.4`)):

```
ansible -i hosts.yaml all -m ping
```

You should get something like the following:

```
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

```
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
