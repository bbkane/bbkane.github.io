# Ben's Corner

My blog

## Install

Follow the [Github instructions](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/), but use the following information:

### Ubuntu 16.04 (my VM)

- Make sure the right port is forwarded to the host in the Vagrantfile before boot:

```
config.vm.network "forwarded_port", guest: 4000, host: 4000
```

- Install dependencies (not using version managers because I can just wipe the VM)

```
sudo apt install ruby ruby-dev nodejs
```

- Ignore this error about html-pipeline

```
-------------------------------------------------
Thank you for installing html-pipeline!
You must bundle Filter gem dependencies.
See html-pipeline README.md for more details.
https://github.com/jch/html-pipeline#dependencies
-------------------------------------------------
```

- Follow the [Github instructions](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/).

### Mac

On Mac, I'm not using a VM, so I need to isolate the processes using version managers.

- Install dependencies

I'm using [nvm](https://github.com/creationix/nvm) so I can use multiple node versions.

```
nvm install node
```

I'm using [rvm](https://github.com/rvm/rvm) so I can use multiple ruby versions

```
rvm install ruby # I had to compile it...

rvm docs generate-ri
```

- Ignore this message

```
----------------------------------------------
Thank you for installing minima 2.0!

Minima 2.0 comes with a breaking change that
renders '<your-site>/css/main.scss' redundant.
That file is now bundled with this gem as
'<minima>/assets/main.scss'.

More Information:
https://github.com/jekyll/minima#customization
----------------------------------------------
```

- Follow the [Github instructions](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/).

## Serve the site

- From a VM, use the `-H, --host` option with the IP of `0.0.0.0` so the site will be reachable from the host.

```
bundle exec jekyll serve --host 0.0.0.0
```

- Go to the site: http://127.0.0.1:4000/

- Possibly use the `-w, --watch` option to rebuild the site on file changes.
- Possibly use the `-D, --drafts` option to serve posts in the `_drafts` folder.

