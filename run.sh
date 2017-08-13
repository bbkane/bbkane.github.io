#!/bin/bash

readonly jekyll_port=4000

# On my Linux VM, Firefox isn't installed.
# TODO: test the jekyll_port stuff
if [[ "$(uname)" == "Darwin" ]]; then
    (echo "Will open the site in 5 sec" && sleep 5 && open "http://127.0.0.1:${jekyll_port}/") &
fi

# This is not only OS dependent (modern Linux), but the primary interface is also machine dependent
if [[ "$(hostname)" == "bbkane-Latitude-E7440" ]]; then
    # gleaned from inspecting ip addr
    readonly primary_interface=wlp2s0
    # https://unix.stackexchange.com/a/8521/185953
    readonly hostname_ip=$(ip -o -4 addr list ${primary_interface} | awk '{print $4}' | cut -d/ -f1)
    echo "Reach the site on the local network at $(tput bold)http://${hostname_ip}:${jekyll_port}$(tput sgr0)"
fi

# If it's taking too long, use `--incremental`, but I've noticed
# that it doesn't rebuild the index page so I'm taking it out for now
bundle exec jekyll serve --host 0.0.0.0 --port "${jekyll_port}" --watch --drafts
