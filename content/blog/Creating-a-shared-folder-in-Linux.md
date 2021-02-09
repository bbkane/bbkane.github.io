+++
title = "Creating a shared folder in Linux"
date = 2017-04-25
updated = 2018-01-09
aliases = [ "2017/04/25/Creating-a-shared-folder-in-Linux.html" ]
+++

Sometimes it's useful to change a folder's setting so multiple users can access it.

Here's how I do that. After this, all members of the group `apache` will be able to create files and directories under `/var/www/html` and those files and directories will retain group permissions.

```bash
# Do all of this as root
# add myself to apache group
# verify this by relogging in and typings `groups`
usermod -a -G apache bbkane

# backup permissions for the folders I'm about to change
# If this goes wrong (recursive commands are dangerous), we can use this
# file to restore those permissions
# See https://unix.stackexchange.com/a/189158/185953
getfacl -R /var/www > /var/www/permissions.facl

# change the group to apache so anybody in that group can edit these files
# and add the sticky bit to anything created under /var/www is also owned by apache
# See https://stackoverflow.com/a/6448326/2958070
cd /var/www/html/
chgrp -R apache .
# Add read, write, execute/search bit to directories (+x means files can be
# accessed when # applied to a directory)
chmod -R g+rwX .
find . -type d -exec chmod g+s '{}' +

# To change it back, restore from the permissions saved earlier
# (I haven't actually had to test this yet)
cd /var/www
setfacl --restore=permissions.facl
```

In addition, if it's a git repo that you're sharing on a server, you should change the following config value:

```
git config core.sharedRepository group
```

to make git create group owned files instead of user owned ones.
