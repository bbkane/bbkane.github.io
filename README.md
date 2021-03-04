from staticsite.md

# TODO

- turn root page into about me and link to blog

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
- figure out how to use images. Test site? See https://www.getzola.org/documentation/content/overview/#asset-colocation
- make sure all vars work on old blog- all of them are for the `{{ site.baseurl }}/path/to/image`
- Is code CSS not working anymore? It looks like it's using a zola built-in one. Rm the original CSS
- port /img/favicon/... images (not sure where they're needed?)
- Push to netlify!

# TODO later

- Get search working
- TELL PEOPLE TO EMAIL ME IF THEY LIKE MY BLOG POSTS!!
- Get "view page source" on GitHub - see https://tera.netlify.app/docs/#macros for macros

# View Page Source

Get "view page source" on GitHub - see https://tera.netlify.app/docs/#macros for macros
I want to be able to add links to edit pages on GitHub

root:
    http://127.0.0.1:1111/
    ./content/_index.md
    https://github.com/bbkane/bbkane.github.io/blob/zola/content/_index.md
section:
    http://127.0.0.1:1111/blog
    ./content/blog/_index.md
    https://github.com/bbkane/bbkane.github.io/blob/zola/content/blog/_index.md
Text post:
    http://127.0.0.1:1111/blog/sad-work-from-home-meals/
    ./content/blog/Sad-Work-from-home-Meals.md
Img Post:
    http://127.0.0.1:1111/blog/my-workstation/
    ./content/blog/My-Workstation/index.md

From https://www.getzola.org/documentation/templates/overview/ - the only thing available is the current_path for all pages.

I don't see anything for it in
https://www.getzola.org/documentation/content/page/ either. This doesn't appear
possible without manually adding metadata in each page. I'm going to abandon it
and maybe propose a "page.filepath" once I've implemented sorting by updated.

---
done with 
