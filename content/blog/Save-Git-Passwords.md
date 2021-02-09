+++
title = "Save Git Passwords"
date = 2016-07-13
updated = 2017-08-04
aliases = [ "2016/07/13/Save-Git-Passwords.html" ]
+++

I save my github usernames on my local machine with the following command:

```bash
git config --global credential.https://github.com.username <my_username>
```

If I mess up the command, I fix it by editing the config file:

```bash
git config --global --edit
```
