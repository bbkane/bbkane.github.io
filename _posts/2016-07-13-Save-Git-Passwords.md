---
layout: post
title: Save Git Passwords
---

I save my github usernames with the following command:

```bash
git config --global credential.https://github.com.username <my_username>
```

If I mess up the command, I fix it by editing the config file:

```bash
git config --global --edit
```