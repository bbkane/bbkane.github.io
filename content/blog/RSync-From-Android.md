+++
title = "RSync From Android"
date = 2017-07-18
updated = 2021-01-17
aliases = [ "2017/07/18/RSync-From-Android.html" ]
+++

Every once in a while, I like to transfer a folder from my Android phone to my Mac. This folder has new content added every once in a while, and the files get large, so I don't want to re-transfer the already-sent files. Rsync is a perfect tool for this. After starting an SSH server with the SSHelper app, I use the following script to rsync the files over.

```bash
#!/bin/bash

remote_user='admin'
remote_host='192.168.1.66' # This isn't a static IP, so this might change once in a while. Check SSHelper output
remote_dir='/path/to/folder/on/phone'

local_dir='/path/to/folder/on/mac'

# exit on errors or unset variables
set -eu

# print commands before executing them
set -x

# these are the options I'm always going to use
# unfortunately, Bash won't really let me put any comments by the options
rsync_minimal() {
rsync \
    -e 'ssh -p 2222' \
    --recursive \
    --verbose \
    --compress \
    --human-readable \
    --stats \
    --progress \
    "$@"
}

# use this to go as fast as possible
rsync_minimal "${remote_user}@${remote_host}:${remote_dir}/" "${local_dir}/"

# use this if I need to not clog up our wi-fi
# rsync_minimal --bwlimit=500 "${remote_user}@${remote_host}:${remote_dir}/" "${local_dir}/"
```

## Bonus

When messing with a  filling filesystem on Android, I like to use the following command to see the biggest 30 files:

```bash
du -ax ./* | sort -k1,1n | tail -n30
```

## Notes from `man rsync`

```
# Notes From `man rsync`
# ---
## rsync slashes on folder names

#   rsync -avz foo:src/bar/ /data/tmp

# A  trailing slash on the source changes this behavior to avoid creating an additional
# directory level at the destination.  You can think of a trailing /  on  a  source  as
# meaning  "copy  the  contents of this directory" as opposed to "copy the directory by
# name", but in both cases the attributes of the containing directory  are  transferred
# to  the containing directory on the destination.  In other words, each of the follow-
# ing commands copies the files in  the  same  way,  including  their  setting  of  the
# attributes of /dest/foo:

#   rsync -av /src/foo /dest
#   rsync -av /src/foo/ /dest/foo

## rsync --archive notes:

#         -a, --archive               archive mode; same as -rlptgoD (no -H)
#         -r, --recursive             recurse into directories
#         -l, --links                 copy symlinks as symlinks
#         -p, --perms                 preserve permissions
#         -t, --times                 preserve times
#         -g, --group                 preserve group
#         -o, --owner                 preserve owner (super-user only)
#         -D                          same as --devices --specials
#         --devices
#               This  option  causes rsync to transfer character and block device files to the
#               remote system to recreate these devices.  This option has  no  effect  if  the
#               receiving rsync is not run as the super-user and --super is not specified.


#         --specials
#               This  option  causes rsync to transfer special files such as named sockets and
#               fifos.

# ---
```

# Rclone

I don't want to make a new blog post for this, but here's a good way to use `rclone` to copy files. Also see the [docs](https://rclone.org/commands/rclone_copy/).

```
rclone \
    --dry-run \
    --progress \
    --log-level DEBUG \
    --log-file ~/tmp_rclone.log.json \
    --use-json-log \
    copy \
    ~/tmp bbkane_onedrive:/tmp
```

