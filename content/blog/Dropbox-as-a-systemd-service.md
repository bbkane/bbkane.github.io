+++
title = "Dropbox as a systemd service"
date = 2017-08-04
updated = 2018-01-02
aliases = [ "2017/08/04/Dropbox-as-a-systemd-service.html" ]
+++

If you've ever worked with Dropbox on Linux, you know that you basically
download a script, untar it, and execute it.

I use the following Ansible task to install it:

```
  - name: Install dropbox
    shell: curl -L "https://www.dropbox.com/download?plat=lnx.x86_64" | tar -C $HOME -xzf -
    args:
      creates: ~/.dropbox-dist/dropboxd
    # For now, I'm just going to manually start it the first time and auth
```

The first time it executes, it asks
for authorization, but, after that, you basically just leave that terminal open
to keep the app working on your machine. This type of long-running program is
called a daemon, and, in many modern distributions of Linux, daemons are  managed with systemd.
You can create a service file, which tells systemd how to treat your daemon,
then tell systemd to start it now, and start it on boot, and you are done.
Fairly easy. I went a-Googling for Dropbox service files and realized all of
them needed root access! When running it manually, there is no need for root
access, so systemd shoudln't need it either. With that sentiment, here is the user
level dropbox systemd service file I came up with (see [the docs](https://www.freedesktop.org/software/systemd/man/systemd.unit.html#Specifiers) for more information).

```conf
[Unit]
Description=Dropbox as a user service
After=local-fs.target network.target

[Service]
Type=simple
ExecStart=%h/.dropbox-dist/dropboxd
Restart=on-failure
RestartSec=1
# Note: don't set these in user mode- they're already set, and
# systemd won't have permission to set them- killing your service before
# it starts
# User=%U
# Group=%U

[Install]
WantedBy=default.target
```

Drop that puppy into `~/.config/systemd/user/dropbox.service`, creating files
and directories as needed.

Start the service with:

```
systemctl --user start dropbox
```

Make sure it worked with:

```
$ systemctl --user status dropbox
● dropbox.service - Dropbox as a user service
   Loaded: loaded (/home/bbkane/.config/systemd/user/dropbox.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2017-08-04 22:01:02 CDT; 1h 48min ago
 Main PID: 1407 (dropbox)
   CGroup: /user.slice/user-1000.slice/user@1000.service/dropbox.service
           └─1407 /home/bbkane/.dropbox-dist/dropbox-lnx.x86_64-31.4.25/dropbox
```

In my (limited) experience, Dropbox tends to be a quiet service, as checking the
logs with journalctl doesn't really produce much

```
$ journalctl -u dropbox
-- No entries --
```

Finally, make sure the service starts on login with:

```
$ systemctl --user enable dropbox
Created symlink /home/bbkane/.config/systemd/user/default.target.wants/dropbox.service → /home/bbkane/.config/systemd/user/dropbox.service.
```
