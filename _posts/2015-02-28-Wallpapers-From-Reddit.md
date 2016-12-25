---
layout: post
title: Wallpapers From Reddit
---

A while back, I found a nice [script](https://github.com/nagracks/reddit_get_top_images) to download wallpapers from Reddit. 
It originally only downloaded wallpapers from one subreddit at a time, so I made a [fork](https://github.com/bbkane/reddit_get_top_images)
to handle multiple subreddits and use a JSON configuration file (the multiple subreddits feature has since been merged into master).

To use it, get a list of subreddits you want to download, and use the `-wc FILENAME` argument to print them to a file (or don't specify it and simply download the images).

My current config file looks like this:

```json
{
    "destination": "~\\Pictures\\reddit_pics",
    "limit": 15,
    "period": "w",
    "separate_dirs": false,
    "subreddit": [
        "earthporn",
        "cityporn",
        "villageporn",
        "architectureporn",
        "abandonedporn",
        "churchporn",
        "roomporn",
        "bookporn",
        "futureporn",
        "imaginarycastles",
        "imaginaryinteriors"
    ]
}
```

Then, run the script again with your new config file (the `-c FILENAME` option) to download the wallpapers!

So far, we have saved wallpapers from Reddit to a folder. What we need to do next will be determined by what operating system we're using.

If you're on Windows 7, I highly recommend [DisplayFusion](http://www.displayfusion.com/), sold through their website or through [Steam](http://store.steampowered.com/app/227260/). This app can configure wallpapers for mulitple monitors and rotate them after a specified time.

If you're on Mac, you can set up your wallpaper in *System Preferences* -> *Desktop and Screen Saver*. Here you can also set up wallpapers to change after a specified time.

On Linux, I use [feh](https://wiki.archlinux.org/index.php/feh) to manage my wallpapers on [i3wm](https://i3wm.org/). My config for it is right [here](https://github.com/bbk1524/backup/blob/master/tower/.i3/config).

I even wrote a small script to just launch the wallpaper getter from a shortcut on my desktop:

```python
import subprocess
import sys
import os

config_path = os.path.join(sys.path[0], 'config.json')
get_top_images_path = os.path.join(sys.path[0], 'get_top_images.py')
if os.path.exists(config_path) and os.path.exists(get_top_images_path):
    subprocess.run(['python', get_top_images_path, '-c', config_path])
else:
    print('Put the right files in %r' % sys.path[0], file=sys.stderr)
```

In regards to the code: I orginally created a class that contained an `argparse.ArgumentParser`. After some consideration, and the realization that
I will probably want to re-use the functionality, I rewrote it to consume the parser as an argument- this separates the parser functionality from the serialization functionality.