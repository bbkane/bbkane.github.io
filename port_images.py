#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import argparse
import re
import shutil
import sys

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
<description>
Examples:
    {sys.argv[0]}
Help:
Please see Benjamin Kane for help.
Code at <repo>
"""


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--src_base_dir", default="~/Git/bbkane.github.io")
    parser.add_argument("--dst_base_dir", default="~/Git/bbkane.github.io-zola")

    return parser.parse_args(*args, **kwargs)


# def rename_img_links(blog_path: Path):
#     blog_text = blog_path.read_text()
#     new_blog_lines = []
#     pattern = r"!\[(.*)\]\(\{\{ site\.baseurl \}\}/"
#     replacement = r"replacement"
#     for line in blog_text.splitlines():
#         new_blog_lines.append(re.sub(pattern, replacement, line))
#     new_blog_text = "\n".join(new_blog_lines)
#     blog_path.with_name("index_fixed_img_links.md").write_text(new_blog_text)


def main():
    args = parse_args()
    src_base_dir = Path(args.src_base_dir).expanduser()
    src_img_dir = src_base_dir / "img"

    dst_base_dir = Path(args.dst_base_dir).expanduser()
    dst_post_dir = dst_base_dir / "content/blog"

    for post_img_dir in src_img_dir.iterdir():
        if not post_img_dir.is_dir():
            print(f"Expected dir: found {post_img_dir!r}", file=sys.stderr)
            continue

        if post_img_dir.name == "favicon":  # TODO: don't forget to port this! Does it need porting
            continue

        name_without_date = post_img_dir.name[11:]
        new_img_dir = dst_post_dir / name_without_date

        shutil.copytree(post_img_dir, new_img_dir, dirs_exist_ok=True)

        renamed_blog = new_img_dir / "index.md"
        if not renamed_blog.exists():
            blog_to_move = dst_post_dir / (name_without_date + ".md")
            blog_to_move.rename(renamed_blog)

        # rename_img_links(renamed_blog)
        # # read file into a string
        # blog_text = renamed_blog.read_text()
        # new_blog_lines = []
        # for line in blog_text.splitlines():
        #         re.sub(
        #             r'\!\[\(.*\)\](\{\{ site\.baseurl \}})
        #         )


if __name__ == "__main__":
    main()
