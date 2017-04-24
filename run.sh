#!/bin/bash

# On my Linux VM, Firefox isn't installed.
if [[ "$(uname)" == "Darwin" ]]; then
    (echo "Will open the site in 5 sec" && sleep 5 && open 'http://127.0.0.1:4000/') &
fi

# If it's taking too long, use `--incremental`, but I've noticed
# that it doesn't rebuild the index page so I'm taking it out for now
bundle exec jekyll serve --host 0.0.0.0 --watch --drafts
