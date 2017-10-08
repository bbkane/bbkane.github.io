---
layout: default
title: Anaconda Python Bash Functions
---

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
