---
layout: default
title: Short BASH Snippets
---

## Run a Server and open a browser with the link

I use a snippet similar to this when I want to open a browser after I run a
blocking command (usually starting a server). I use this particular example to
learn Elm. I have something similar to run Jekyll for my blog.

```bash
learn_elm() {
    cd ~/Code/Elm || echo "Non-existant dir"
    code .
    if [[ "$(uname)" == "Darwin" ]]; then
        open_command=open
    elif [[ "$(uname)" == "Linux" ]]; then
        open_command=xdg-open
    fi
    # Open a subshell in a fork
    (sleep 2 && "${open_command}" "http://127.0.0.1:8000") &
    # Run the blocking command
    elm reactor
}
```

## Simple but effective backup command.

```bash
bak() {
    date_string="$(date +'%Y-%m-%d.%H.%M.%S')"
    if [[ -d "$1" ]]; then
        local -r no_slash="${1%/}"
        cp -r "${no_slash}" "${no_slash}.${date_string}.bak"
    elif [[ -f "$1" ]]; then
        cp "$1" "${1}.${date_string}.bak"
    else
        echo "Only files and directories supported"
    fi
}
```

## BASH script starter

```bash
#!/bin/bash

# exit the script on command errors or unset variables
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

# https://stackoverflow.com/a/246128/295807
# readonly script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# cd "${script_dir}"
```
