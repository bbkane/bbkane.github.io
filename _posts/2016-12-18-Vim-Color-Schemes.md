---
layout: default
title: Vim Color Schemes
---

One of the joys of [Neo]Vim is the amount of color schemes available. The editor
ships with several colorschemes by default, but adding more is what Vim was made
to do!

Before we begin, know that Vim, NeoVim, and the various terminals they work with
can be finicky with colors. On Windows, I'm using
[neovim-qt](https://github.com/equalsraf/neovim-qt). On Mac, I'm using MacVim
or iTerm2 with NeoVim. On Linux I'm using LXTerminal on Ubuntu 16.04 with
NeoVim. The following notes with with my setup.

There are a couple of notes to keep in mind when using colorschemes:

- Some terminals do not support some colors. A nice overview of this can be
  found in one of my favorite colorscheme's
  [documentation](https://github.com/morhetz/gruvbox/wiki/Terminal-specific)
- Sometimes (on Windows/Mac, but oddly not on my Linux) `termguicolors` should
  be set. See `:help termguicolors` for more information
- Your background can be light or dark and many colorschemes with adjust. I
  universally prefer a dark background so I always `set background=dark`.

Because I work on several servers/VMs that don't have NeoVim or
[vim-plug](https://github.com/junegunn/vim-plug) installed, or all the features
I prefer on my main development machines, I have to be careful to avoid or
handle any missing features or errors that might arise. I need to be able to
scp my vim initialization file to a machine and just use it. With this in
mind, the main thrusts of this post are to document how I use features when
available but gracefully fall back to good defaults, my favorite colorscheme
plugins, and how to change the colorscheme for new Vim instances from the
command line.

# Diverse Features, One Configuration

The first trick I use to (borrowed from somewhere on StackOverflow) is
to use a `try/catch` block to set a default colorscheme if my plugin
colorscheme isn't able to be loaded:

```vim
" Try to use a colorscheme plugin
" but fallback to a default one
try
    colorscheme gruvbox
catch /^Vim\%((\a\+)\)\=:E185/
    " no plugins available
    colorscheme elflord
endtry
```

Likewise, `termguicolors` can be detected using an `if` block:

```vim
" Linux has termguicolors but it ruins the colors...
if has('termguicolors') && (has('mac') || has('win32'))
    set termguicolors
endif
```

I'm sure if I put some more work into it, I could change LXTerminal's settings
to work with Vim, but... I haven't.

# Colorscheme Plugins!

I used the builtin `elflord` colorscheme for quite a while, and I still do
occasionally, but here are some colorscheme plugins I really like (TODO: get pictures):

- [jellybeans](https://github.com/nanotech/jellybeans.vim)
- [molokai](https://github.com/tomasr/molokai)
- [dracula](https://github.com/dracula/vim)
- [railscasts](https://github.com/jpo/vim-railscasts-theme)
- [desert-warm-256](https://github.com/rainux/vim-desert-warm-256)
- [gruvbox](https://github.com/morhetz/gruvbox)

I've also come across a few plugins that add many colorschemes at once!

- [vim-colorschemes](https://github.com/flazz/vim-colorschemes)
- [base16.nvim](https://github.com/Soares/base16.nvim)

That last NeoVim specific plugin can be wrapped in an `if` block:

```
if has('nvim')
    Plug 'Soares/base16.nvim'
endif
```

Tons of colorschemes are now available, so having a plugin that can quickly switch
between them is practically necessary. I use
[`vim-colorscheme-switcher`](https://github.com/xolox/vim-colorscheme-switcher).
With this gem of a plugin, the `F8` key switches to the next colorscheme
available and the `:RandomColorScheme` command becomes available. Unfortunately,
Vim wasn't designed to cleanly switch colorschemes, so sometimes they won't load
properly. [This](https://github.com/xolox/vim-colorscheme-switcher#known-problems) section
of the README explains further.

# Colorschemes before startup (untested on Windows)

With this menagerie of colorschemes, editing an initialization file each time a
color scheme deserves to be changed can become annoying. I used to have a long
list of commented-out colorscheme lines in my `init.vim`, but recently I've
found a way to mitigate the problem- setting the colorscheme from the terminal.

The "hook" between the terminal and Vim can be created using environmental
variables- set an environmental variable in the terminal, and read it in Vim on
startup to do things. I prefix all such environmental variables with `vim_`, so
`vim_colorscheme` is the variable I chose. I use the `try/catch` block described
earlier to catch and handle errors.

```vim
" Try to use a colorscheme plugin
" but fallback to a default one
try
    " get the colorscheme from the environment if it's there
    if !empty($vim_colorscheme)
        colorscheme $vim_colorscheme
    else
        colorscheme gruvbox
    endif
catch /^Vim\%((\a\+)\)\=:E185/
    " no plugins available
    colorscheme elflord
endtry
set background=dark
```

Now in BASH/ZSH I can define a function to easily set a colorscheme:

```bash
set_vim_colorscheme()
{
    export vim_colorscheme="$1"
}
```

I don't have an encyclopedic knowledge of the colorschemes I want, so I also
define a completion function with the colorschemes I like (drop this in
`~/.bashrc` or `~/.zshrc`)

```bash
# make zsh emulate bash if necessary
if [[ -n "$ZSH_VERSION" ]]; then
    autoload bashcompinit
    bashcompinit
fi

# make the autocompletions
# https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion-Builtins.html
_vim_colorschemes='abbott elflord gruvbox desert-warm-256 elflord railscasts dracula 0x7A69_dark desertedocean'
complete -W "${_vim_colorschemes}" 'set_vim_colorscheme'
```

After sourcing these functions, I can use `set_vim_colorscheme  <TAB>` to get a
nice list of colorschemes. One note: when I use tab completion to
auto-complete the command `set_vim_colorscheme` itself, I have to type SPACE
before TAB to convince BASH that the colorscheme is ready for completion.

With graceful feature usage, lot of colorschemes, and the ability to switch them
easily from inside Vim and outside Vim, my sense of style is satisfied and my
ability to procrastinate is enhanced.

I keep my Vim/NeoVim configurations on [GitHub](https://github.com/bbkane/nvim).
