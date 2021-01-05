---
layout: default
title: Short BASH Snippets
---

## BASH script starter

I put this at the top of all my scripts because most of the time I want scripts to fail on errors, and half the time I want the script to run in the directory it's in.

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

## Get the full path to a file

This is perl wrapped in Bash, but it's cross-platform and works on Mac and Linux. The alternative, `readlink -f` doesn't work on Mac.

```bash
fullpath() {
    local -r full=$(perl -e 'use Cwd "abs_path";print abs_path(shift)' "$1")
    echo "$full"
}
```

## Print a BASH command

This snippet prints the command before running it. Stolen from [StackOverflow](https://stackoverflow.com/a/19226038). Great for debugging!

```bash
set -x
command
{ set +x; } 2>/dev/null
```


## Generate and use colored print commands

Running scripts with colored output can make them much friendlier. Consider taking out the newlines if you want nested color prints. I almost never do, so I'm leaving them in...

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

## Run a shell command on file change

I like to use [`entr`](http://www.entrproject.org/) for this. Generate some filenames and pipe them to `entr`. The `-c` option clears the screen and the `-s` option means use the shell.

```bash
ls log.txt | entr -c -s 'date && tail log.txt'
```

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

## Simple Task Runner

For when you want to run some long commands with a shortcut. It does very limited arg parsing.

```bash
print_help(){
    cat << EOF
Workflow:
    $0 first|1
    $0 second|2
EOF
}

first() {
    echo "I'm first"
}

second() {
    echo "I'm second!"
}

set +u
if [ -z ${1+x} ]; then
    print_help
fi
set -u

case "$1" in
    first|1)
        first
    ;;
    second|2)
        second
    ;;
    *)
        echo "Unmatched command: $1"
        print_help
    ;;
esac
```

## Tee `stderr` and `stdout`to files

Save both `stderr` and `stdout` to a file. Only works in Bash. From StackOverflow

```bash
# https://stackoverflow.com/a/59435204
{ { time ./tmp_import.sh | tee tmp_import_log.stdout;} 3>&1 1>&2 2>&3- | tee tmp_import_log.stderr;} 3>&1 1>&2 2>&3-
```

## Process each line on a file

From [Unix StackExchange](https://unix.stackexchange.com/a/580545/185953). I like to combine it with printing the command used.

```bash
while IFS='' read -r line || [ -n "${line}" ]; do
    set -x
    echo "$line"
    { set +x; } 2>/dev/null
done < ./file.txt
```

You can also pipe lines to the while loop:

```bash
pbpaste | while IFS='' read -r line || [ -n "${line}" ]; do
    echo "line: $line"
done
```
