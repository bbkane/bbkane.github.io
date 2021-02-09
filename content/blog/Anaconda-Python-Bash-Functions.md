+++
title = "Anaconda Python Bash Functions"
date = 2017-10-07
updated = 2017-12-21
aliases = [ "2017/10/07/Anaconda-Python-Bash-Functions.html" ]
+++

## Conda Env Management

I use conda for all of my Python projects. Because I'm so often making a project
directory, then making a conda environment with the same name, I've created the
following code to ease the process.

```bash
# Create a conda environment with the same name as the current dir
# Example: conda_create_pwd flask Flask-WTF
conda_create_pwd() {
    conda create --name "$(basename $(pwd))" python=3 "$@"
}
```

```bash
# take advantage of the fact that the conda env is the same
# as the current dir most of the time
alias source_activate_pwd='source activate $(basename $(pwd))'
```

For many projects, I like to have a run script with the following code to
automatically activate the environment

```bash
#!/bin/bash

# exit the script on command errors or unset variables
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

# https://stackoverflow.com/a/246128/295807
readonly script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${script_dir}"

env_name="$(basename $(pwd))"

set +eu
if [[ "${CONDA_DEFAULT_ENV}" != "${env_name}" ]]; then
    # shellcheck disable=SC1091
    source activate "${env_name}"
fi
set -eu

# actual application code here, now that I'm in the correct dir
# with the correct python
```

## Anaconda Python Management

On Mac, I use `brew` to manage package installation. `brew` expects Python
version 2, so I put the following code in my Bash initialization files to
easily switch between versions.

```bash
# Making anaconda functional so I can rm it when homebrew whines
anaconda_bin_dir="$HOME/anaconda3/bin"
add_anaconda() {
    if [[ "$PATH" != *"${anaconda_bin_dir}"* ]]; then
        export PATH="${anaconda_bin_dir}:$PATH"
    fi
}

# add it by default
add_anaconda
```

```bash
rm_anaconda() {
    export PATH=$(echo $PATH | sed 's|'"${anaconda_bin_dir}:"'||g')
}
```
