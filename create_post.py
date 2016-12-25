#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
create_post.py

Author: Benjamin Kane
License: MIT
"""

from os.path import join as p_join
import argparse
import datetime
import os
import subprocess
import sys
import time
import shutil

try:
    import pyperclip
except ImportError:
    use_pyperclip = False
else:
    use_pyperclip = True


# the path where this script resides
ROOT = sys.path[0]

REFRESH_RATE = 1
IMG_ROOT = 'img'
POST_ROOT = '_posts'

default_editor = os.getenv('EDITOR')
if default_editor and shutil.which(default_editor):
    EDITOR = default_editor
elif shutil.which('code'):
    EDITOR = 'code'
elif shutil.which('nvim'):
    EDITOR = 'nvim'
elif shutil.which('vim'):
    EDITOR = 'vim'
else:
    EDITOR = None


def main():
    parser = argparse.ArgumentParser(description="Easily add image links to a jekyll site")
    parser.add_argument('post_name', default=None, nargs='?',
                        help="Name of Post. Ex: 'My Awesome Post'. \
                        If not provided, the script will prompt for it")
    parser.add_argument('-r', '--root', default=ROOT,
                        help="Root of jekyll blog. Ex: /home/bbkane/bbkane.github.io")
    parser.add_argument('-ir', '--image_root', default=IMG_ROOT,
                        help="Folder in jekyll blog that contains images. Ex: img")
    parser.add_argument('-pr', '--post_root', default=POST_ROOT,
                        help="Folder in jekyll blog that contains posts. Ex: _posts")
    parser.add_argument('-rr', '--refresh_rate', default=REFRESH_RATE, type=int,
                        help="Number of seconds per check. Ex: 1")
    parser.add_argument('-e', '--editor', default=EDITOR,
                        help="Editor to open new post in. Must be added to path. Ex: vim")
    args = parser.parse_args()
    if not args.post_name:
        args.post_name = input("Enter the name of your post to create: ")

    # erase empty child folders in img_dir
    img_dir = p_join(args.root, args.image_root)
    for entry in os.scandir(img_dir):
        dir_path = p_join(img_dir, entry.name)
        if entry.is_dir() and not os.listdir(dir_path):
            print('Erasing empty dir: ', dir_path)
            os.rmdir(dir_path)

    # jekyllify filename and create with layout info
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    post_title = today + '-' + args.post_name.replace(' ', '-')
    post_dir = p_join(args.root, args.post_root)
    post_path = p_join(post_dir, post_title + '.md')
    if not os.path.isfile(post_path):
        print('Creating new blog:', post_path)
        with open(post_path, 'w') as post:
            write = lambda s: print(s, file=post) # flake8: noqa
            write('---')
            write('layout: default')
            write('title: ' + args.post_name)
            write('---')
            write('')
    else:
        print(post_path, 'already created.')

    if args.editor:
        try:
            retcode = subprocess.call([args.editor, post_path], shell=False)
            if retcode != 0:
                print("Child was terminated by signal", retcode, file=sys.stderr)
            else:
                print(args.editor, 'opened', post_path, 'successfully')
        except OSError as e:
            print("Execution failed:", e, file=sys.stderr)
    else:
        print('No editor found. configure $EDITOR or use `--editor` flag')

    # create post_img_dir
    post_img_dir = p_join(img_dir, post_title)
    print('Creating new image dir:', post_img_dir)
    os.makedirs(post_img_dir, exist_ok=True)

    if use_pyperclip:
        print('Watching', post_img_dir, 'for changes to make links from them. Ctrl-C quits.')
        # keep checking post_img_dir for changes
        img_list = set(os.listdir(post_img_dir))
        while True:
            time_start = time.time()
            new_img_list = set(os.listdir(post_img_dir))

            # make new files in the dir into links for clipboard
            if new_img_list != img_list:
                links_to_create = new_img_list - img_list
                for img in links_to_create:
                    parts = ('![]({{ site.baseurl }}', args.image_root, post_title, img+')')
                    link = '/'.join(parts)
                    print('Copying link to clipboard:', link)
                    pyperclip.copy(link)
                img_list = new_img_list

            # sleep until we need to refresh
            duration = time.time() - time_start
            if duration < args.refresh_rate:
                time.sleep(args.refresh_rate - duration)
    else:
        print("Install pyperclip for clipboard support")


if __name__ == '__main__':
    main()
