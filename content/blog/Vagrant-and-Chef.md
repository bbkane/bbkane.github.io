+++
title = "Vagrant and Chef"
date = 2016-06-23
updated = 2020-03-20
aliases = [ "2016/06/23/Vagrant-and-Chef.html" ]
+++

# Using Vagrant to play with Chef

I'm using chef to provision some machines from Windows, and here's the process I did it with:

## On Windows

[Install](https://github.com/bbkane/backup/blob/master/windows/install_choco.cmd) choco
and a modern Powershell.

Install vagrant, virtualbox, rsync.

Make a folder and switch to it: `mkdir $env:USERNAME\Vagrant\chef && cd $env:USERNAME\Vagrant\chef`

Use the Vagrantfile modified from this SuperUser [post](http://superuser.com/questions/671191/how-to-ssh-between-a-cluster-of-vagrant-guest-vms).

```ruby
Vagrant.configure(2) do |config|
    config.vm.define "chefworkstation" do |chefworkstation|
        chefworkstation.vm.box = "centos/7"
        config.vm.synced_folder '.', '/vagrant', disabled: true
        # You may wish to use a more obscure private ip, like 10.2.2.4
        chefworkstation.vm.network "private_network", ip: "10.0.0.200"
        chefworkstation.vm.hostname = "chefworkstation1"
    end
    # It's going to be easier to use hosted chef until I need something like this
    # config.vm.define "chefserver" do |chefserver|
    #     chefserver.vm.box = "centos/7"
    #     config.vm.synced_folder '.', '/vagrant', disabled: true
    #     # You may wish to use a more obscure private ip, like 10.2.2.5
    #     chefserver.vm.network "private_network", ip: "10.0.0.201"
    #     chefserver.vm.hostname = "chefserver1"
    #     chefserver.memory = 4096
    # end
    config.vm.define "chefnode" do |chefnode|
        chefnode.vm.box = "centos/7"
        config.vm.synced_folder '.', '/vagrant', disabled: true
        # You may wish to use a more obscure private ip, like 10.2.2.5
        chefnode.vm.network "private_network", ip: "10.0.0.202"
        chefnode.vm.hostname = "chefnode1"
    end
end
```

Start it: `vagrant up`. Because rsync didn't like my SSH settings, I had to do this a couple of times.

SSH into workstation: `vagrant ssh workstation`

## On workstation (known as aharriwinvm on my machine)

Following the instructions from [here](https://learn.chef.io/manage-a-node/rhel/get-set-up/) and [here](https://docs.chef.io/install_dk.html#review-prerequisites).

Download the chefdk installer from the [website](https://downloads.chef.io/chef-dk/redhat/):
`curl -LO https://packages.chef.io/stable/el/7/chefdk-0.15.15-1.el7.x86_64.rpm`

Install it: `sudo rpm -ivh <rpm_name>.rpm`

verify it: `chef verify`

Set up text editor (I'm a vim user):

```
sudo yum -y install vim-enhanced # also installs perl...?
curl -o ~/.vimrc -L https://raw.githubusercontent.com/bbkane/backup/master/common/.vimrc-ben
```

To be continued...

Probably not continued :) :) :)
