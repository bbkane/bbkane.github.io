+++
title = "Clearing Large Files"
date = 2017-01-23
updated = 2017-12-26
aliases = [ "2017/01/23/Clearing-Large-Files.html" ]
+++

I have a couple methods to clear large files. First of all, if the files are repetitive, `logrotate` looks to be the best way to roll.

If not using logrotate though, here's a few methods I've found.

First, see how much space you have:

```bash
df -h
```

See the biggest files and folders:

```bash
see_biggest() {
    if [[ "$(uname)" == "Darwin" ]]; then
        # Macs don't have -h so we sort numerically
        du -ax ./* | sort -n | tail -n "${1-50}"
    elif [[ "$(expr substr $(uname -s) 1 5)" == "Linux" ]]; then
        # Do something under GNU/Linux platform
        du -ahx ./* | sort -h | tail -n "${1-50}"
    fi
}

```

I used the following command to erase the biggest files in a folder except the last two (which I wanted to deal with specially)

```bash
for file in $(see_biggest 10 | awk '{print $2}' | head -n-2); do \rm $file; done
```

This command erases files last modified over 6 months ago (this should probably be run with `-exec echo {} +` before jumping to the `rm`)

```bash
find -type f -mtime +180 -exec rm {} +
```

If I have a big file and I want to delete the first half of it, I use the following command:

```bash
#!/bin/bash

# script name: print_last_half.sh

set -eu

filename="$1"
[[ -z "$filename" ]] && echo "Need filename!" && exit
lines=$(wc -l "$filename" | awk '{print $1}')
last_lines=$(expr "$lines" / 2)
unset lines
tail -n "$last_lines" "$filename"
```

```bash
# Alternative from Andrew
`tail -n $(($(wc -l <filename> | cut -d ' ' -f 1) / 2)) <filename>`
```

Then use it like the following:

```bash
./print_last_half.sh filename.txt filename.txt.lasthalf
# make sure it looks good using `less`
mv filename.txt.lasthalf filename.txt
```


