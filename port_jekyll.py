#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from subprocess import run
import argparse
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

dst_front_matter = (
    """
+++
title = "{title}"
date = {date}
updated = {updated}
aliases = [ "{alias}" ]
+++
""".strip()
    + "\n"
)


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--src_base_dir", default="~/Git/bbkane.github.io")
    parser.add_argument("--dst_base_dir", default="~/Git/bbkane.github.io-zola")

    return parser.parse_args(*args, **kwargs)


def main():
    args = parse_args()
    src_base_dir = Path(args.src_base_dir).expanduser()
    src_post_dir = src_base_dir / "_posts"

    dst_base_dir = Path(args.dst_base_dir).expanduser()
    dst_post_dir = dst_base_dir / "content/blog"

    for f in src_post_dir.iterdir():
        if f.suffix != ".md":
            print(f"Unknown thing in {src_post_dir}: {f!r}", file=sys.stderr)

        with f.open() as fp:
            lines = fp.readlines()
        is_standard_front_matter = (
            (lines[0] == lines[3] == "---\n") and lines[1] == "layout: default\n" and lines[2].startswith("title: ")
        )

        # port front matter
        if not is_standard_front_matter:
            print(f"Non-standard front matter: {f}", file=sys.stderr)
            continue
        title = lines[2][7:].strip()
        date = f.name[0:10]

        # Run git to see when this file was last commited to
        # For some reason, the 'format:' part doesn't disappear (despite what git log --help says)
        # I can work around this by simply not including it
        # updated_cmd = ["git", "log", "-1", '--pretty="format:%cs"', str(f)]
        updated_cmd = ["git", "log", "-1", "--pretty=%cs", str(f)]
        updated_result = run(
            updated_cmd,
            cwd=str(f.parent),
            capture_output=True,
        )
        if updated_result.returncode != 0:
            raise SystemExit(f"git log error: {f}: {updated_cmd}\n{updated_result.stderr}")
        updated = updated_result.stdout.decode("utf-8").strip()

        alias = str(f.with_suffix(".html").name)
        alias = alias.replace("-", "/", 3)

        # remove the original blog directory, take the date out of the file
        # name, and put it into the dst blog directory
        new_blog_path = dst_post_dir / f.relative_to(src_post_dir).with_name(f.name[11:])
        with new_blog_path.open("w") as fp:
            fp.write(
                dst_front_matter.format(
                    title=title,
                    date=date,
                    updated=updated,
                    alias=alias,
                )
            )
            fp.writelines(lines[4:])

        # break


if __name__ == "__main__":
    main()
