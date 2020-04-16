---
layout: default
title: Long Shell Oneliners Without the Pain
---

I love working in my terminal. It has a ton of useful programs that you can stitch together to do useful things. However, sometimes these commands can get long. For example, here's a command I use to [launch a Jupyter Notebook in docker](https://www.bbkane.com/2018/10/24/Jupyter-Lab-on-Docker.html):

```bash
docker run --rm --user "$UID" --group-add users -p 8888:8888 -v "$HOME/Code/Jupyter:/home/jovyan/work" jupyter/scipy-notebook start.sh jupyter lab --NotebookApp.password="$password_hash"
```

That command is a pain to type out! However, once it's typed out and in my history, I can use `Ctrl + r` to search for it (I even have [`fzf`](https://github.com/junegunn/fzf) set up so I can fuzzy search my history!). Now it's ready to be run again and I didn't have to type it all out.

But... what if I need to change the port it's running on from 8888 to 8000? I can use `Ctrl + a` to go to the beginning, or `Ctrl + e` to go to the end of the line, but the port stuff is in the middle, and I'm stuck arrow-keying my way to get to it .In fairness, there are keyboard shortcuts to go back/forward a word at a time, and probably other shortcuts, but I can never remember them.

One thing I can do is hit `Ctrl + x, Ctrl + e` to open up my `$EDITOR` (`NeoVim`) to edit the long command. Now I can use all of Vim's tricks to edit my command. But I'm still faced with the problem of it being all in one line, hard to read and not super nice to edit.

I was tediously running a lot of these similar but not the same long commands one day and inspiration struck. What if I turned the command from one line to many lines? Then I could more easily read and edit it. That night, I wrote [an auto-formatter for shell commands](https://github.com/bbkane/dotfiles/blob/master/bin_common/bin_common/format_shell_cmd.py) and the next week or so, when time permitted, I made it accessible from a [Vim Command](https://github.com/bbkane/dotfiles/blob/91ac752ac4a25eca1f3ff271249d2e5878b265b2/nvim/.config/nvim/init.vim#L397). Now, when I open up Vim to edit a commnd, I can `:FormatShellCmd` it, and it makes it multiline!

```bash
docker run \
    --rm \
    --user "$UID" \
    --group-add users \
    -p 8888:8888 \
    -v "$HOME/Code/Jupyter:/home/jovyan/work" jupyter/scipy-notebook start.sh jupyter lab \
    --NotebookApp.password="$password_hash"
```

This is much easier to edit!

## See it in action!

As a side note, check out my `zsh` customizations [here](https://github.com/bbkane/dotfiles/blob/master/zsh/README.md).

![]({{ site.baseurl }}/img/2020-04-14-Long-Shell-Oneliners-Without-the-Pain/oneline-edit.2.gif)

## Comments

This really took off on Reddit. Feel free to add a [comment there](https://www.reddit.com/r/vim/comments/g1lx7e/i_made_a_command_to_autoformat_shell_commands/)!
