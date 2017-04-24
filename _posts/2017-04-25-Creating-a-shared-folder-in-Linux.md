---
layout: default
title: Creating a shared folder in Linux
---

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
getfacl -R /var/www > /var/www/permissions.facl

# change the group to apache so anybody in that group can edit these files
# and add the sticky bit to anything created under /var/www is also owned by apache
chgrp -R apache /var/www/html/
chmod -R u+rwx,g+rws /var/www/html
```

