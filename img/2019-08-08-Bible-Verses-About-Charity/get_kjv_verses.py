#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import urllib.parse
import urllib.request

template = """
## [{verse_ref}]({verse_ref_url})

{content}
"""


with open("verses.txt") as fp, open("output.md", "w") as ofp:
    for line in fp:
        line = line.strip()
        if not line:
            continue

        headers = {"Content-Type": "application/json"}
        line = urllib.parse.quote(line)
        url = f"https://bible-api.com/{line}?translation=kjv"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            return_code = resp.getcode()
            headers = resp.info()

        obj = json.loads(content)

        book_id = obj["verses"][0]["book_id"]
        chapter = obj["verses"][0]["chapter"]
        verse_ref_url = f"https://www.bible.com/bible/1/{book_id}.{chapter}.KJV"
        output = template.format(
            verse_ref=obj["reference"],
            verse_ref_url=verse_ref_url,
            content=obj["text"].strip(),
        )
        print(output, file=ofp)
        time.sleep(0.5)
