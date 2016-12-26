# Ben's Corner

My blog

## Install

Follow the [Github instructions](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/), but use the following information:

### Ubuntu 16.04 (my VM)

- Make sure the right port is forwarded to the host in the Vagrantfile before boot:

```
config.vm.network "forwarded_port", guest: 4000, host: 4000
```

- Install dependencies

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

- From a VM, use the `-H, --host` option with the IP of `0.0.0.0` so the site will be reachable from the host.

```
bundle exec jekyll serve --host 0.0.0.0
```

- Go to the site: http://127.0.0.1:4000/

- Possibly use the `-w, --watch` option to rebuild the site on file changes.
- Possibly use the `-D, --drafts` option to serve posts in the `_drafts` folder.
