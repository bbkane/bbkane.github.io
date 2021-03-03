from staticsite.md

# TODO

- figure out how to use images. Test site? See https://www.getzola.org/documentation/content/overview/#asset-colocation
- make sure all vars work on old blog- all of them are for the `{{ site.baseurl }}/path/to/image`
- Is code CSS not working anymore? It looks like it's using a zola built-in one. Rm the original CSS
- Get "view page source"
- TELL PEOPLE TO EMAIL ME IF THEY LIKE MY BLOG POSTS!!
- Get search working
- turn root page into about me and link to blog
- port /img/favicon/... images (not sure where they're needed?)

# Done

- get word count - done
- port mds - done
- Get Google Site-Analytics working - done
- get root page working - done
- get code blocks not one-liners - done
- get content truncated in index - done
- get empty links filled `/\[.*\]()` - done
- Sort by updated not working?? - made https://github.com/getzola/zola/issues/1384 to try to get this supported
- Why does zola serve work but zola build not? - HTML expects a root. Building and starting a local server in that directory fixes this.

# Image porting notes

- Test image!! - done and works fine
- go through directories in /img/
- get blog file names (rm date) and cp img directory with the new name into blog/
- mv blog/post_name.md into /blog/post_name/index.md

Use sed or something to fix up the regex
