---
layout: default
title: Changing words quickly with Vim
---

Today, while walking a user through an internal README, she mentioned that she
wanted commands to type surrounded by backticks (`` `type me` ``), (which `makes
it look like code`), and filenames surrounded with quotes (`"filename.txt"`). I
thought changing words like this would be a lot more tedious than it turned out
to be.


I ended up making this change with the following Vim usage:

- Install [vim-surround](https://github.com/tpope/vim-surround) to help change
  surrounding text.
- Travel to possible filenames surrounded by backticks
  - Turn on search highlighting with `:set hlsearch`
  - Search for words with a `.` surrounded by backticks with the following
    search: `` /`.*\..*` ``
  - This search will pull up more matches than we want to change, so travel
    between them with `n` and `N`.
- Once the cursor is on the first word to chagne, type `` cs`" `` to change the
  surrounding backticks to quotes.
- Hit `n` to go to the next potential word to change and, if it's something to
  change, hit `.` to repeat the last change.

In the end, once you set up the search and the change, actually changing the
rest of the document consists of typing `n` , then `.` for each word. Short of
writing a script specifically to read a file, present possible matches, prompt
me whether or not to replace them, and then change it (which would take way more
set up), I can't think of another way to easily change large amounts of text in
this manner.
