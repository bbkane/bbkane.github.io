---
layout: default
title: RSync From Android
---

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