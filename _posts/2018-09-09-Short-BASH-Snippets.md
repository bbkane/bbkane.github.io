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

## Expand a BASH command

Stolen from [StackOverflow](https://stackoverflow.com/a/19226038)

```bash
set -x
command
{ set +x; } 2>/dev/null
```

## Run a shell command on file change

I like to use [`entr`](http://www.entrproject.org/) for this. Generate some filenames and pipe them to `entr`. The `-c` option clears the screen and the `-s` option means use the shell.

```bash
ls log.txt | entr -c -s 'date && tail log.txt'
```

## Generate and use colored print commands



Consider taking out the newlines if you want nested color prints. I almost never do, so I'm leaving them in...

### Define the function factory

```bash
make_print_color() {
    color_name="$1"
    color_code="$2"
    color_reset="$(tput sgr0)"
    if [ -t 1 ] ; then
        eval "print_${color_name}() { printf \"${color_code}%s${color_reset}\\n\" \"\$1\"; }"
    else  # Don't print colors on pipes
        eval "print_${color_name}() { printf \"%s\\n\" \"\$1\"; }"
    fi
}
```

### Generate pretty print functions and use them

```bash
make_print_color "red" "$(tput setaf 1)"
make_print_color "green" "$(tput setaf 2)"
make_print_color "yellow" "$(tput setaf 3)"

print_red "Always"
print_green "Seeing"
print_yellow "in Color!"

# print to stderr: https://stackoverflow.com/a/2990533/2958070
print_red "Error!" >&2
```
