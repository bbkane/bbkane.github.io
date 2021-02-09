+++
title = "Changing words quickly with Vim"
date = 2017-08-11
updated = 2017-10-15
aliases = [ "2017/08/11/Changing-words-quickly-with-Vim.html" ]
+++

I try to use Vim shortcuts to automate repetitive text-editing tasks. Here are
two examples.

## Differentiating Code and Files

While walking a user through an internal README, she mentioned that she
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

## Vimifying pasted Docs

Sometime last year I started doing most text editing in Vim. I was recently
copying text from multiple Google Docs documents into Vim and I wanted to make
the text friendly to work with in Vim. This means that I wanted to separate
paragraphs with a space, remove leading indentation from paragraphs, and insert
newlines to separate long lines (I like my lines 80 characters wide).

This is fairly easy to do manually. When copied the paragraphs were already
separated by spaces, so I didn't have to do that. Unindenting an offending line
can be done with `<<` and formatting it with newlines can be done with `gqq`.
But doing those steps can be automated even further with [macros]
(http://vim.wikia.com/wiki/Macros):

- Navigate to an offending line in Normal Mode
- `qa` to start recording a macro in the `a` register
- `<<` to unindent the line
- `gqq` to impose my line length
- `o` to insert a new line and inter Insert Mode
- `<Esc>` to exit Insert Mode to Normal Mode
- `j` to move down a line
- `q` to stop recording

Now I can play that macro with `@a` in Normal Mode. That's still awkward to
type, so I temporarily remapped it to Space in Normal Mode with
`:nnoremap <Space> @a`.

Now formatting the document is pretty easy. Go to a line, then hit `<Space>` to
format it. The macro takes me to the next line after that, so there's a good
chance I can just hit `<Space>` again.
