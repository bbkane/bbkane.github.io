+++
title = "Simple Blog Post Stats"
date = 2017-10-08
updated = 2017-10-08
aliases = [ "2017/10/08/Simple-Blog-Post-Stats.html" ]
+++

I got curious about the word count in my blog. When I generate the static site,
I simply count whitespace separated strings as words, but this will
automatically include code sections. To find out how much prose I wrote, I need
to process each blog post, ignoring the front-matter (information at the top of
each post and surrounded by `---`) and the code sections (which are surrounded
by three tildes), and adding valid words to my statistics (I'm just keeping a
total word count and count of each word). I got some the following results:

Word Count:  7089

Wow! Over 7000 words! I'm pretty happy with that!

| order | word | count |
|=======|======|=======|
| 1 | the | 402 |
| 2 | to | 296 |
| 3 | a | 196 |
| 4 | i | 172 |
| 5 | and | 155 |
| 6 | it | 122 |
| 7 | this | 109 |
| 8 | of | 106 |
| 9 | is | 93 |
| 10 | in | 91 |
| 11 | with | 86 |
| 12 | that | 83 |
| 13 | for | 66 |
| 14 | on | 65 |
| 15 | my | 65 |
| 16 | you | 52 |
| 17 | from | 52 |
| 18 | be | 50 |
| 19 | use | 47 |
| 20 | can | 43 |
| 21 | so | 38 |
| 22 | if | 35 |
| 23 | we | 35 |
| 24 | file | 31 |
| 25 | command | 31 |
| 26 | site.baseurl | 30 |
| 27 | then | 29 |
| 28 | powershell | 29 |
| 29 | but | 28 |
| 30 | are | 28 |
| 31 | have | 28 |
| 32 | like | 28 |
| 33 | by | 27 |
| 34 | following | 26 |
| 35 | an | 26 |
| 36 | now | 25 |
| 37 | one | 25 |
| 38 | will | 24 |
| 39 | some | 24 |
| 40 | or | 24 |
| 41 | at | 24 |
| 42 | install | 23 |
| 43 | up | 23 |
| 44 | using | 23 |
| 45 | your | 22 |
| 46 | when | 22 |
| 47 | get | 21 |
| 48 | do | 21 |
| 49 | want | 21 |
| 50 | also | 21 |

Well, this was a lot more disappointing. I don't use a lot of interesting words,
I assume.

## Code

I used the following code to generate this:

```python
#!/usr/bin/env python3

from collections import Counter
from pathlib import Path
import string
import sys

# This script goes through my _posts directory, strips
# out lines surrounded by ``` or --- blocks, then does a little
# statistics on the results


def is_valid_word(word):
    contains_letters = any(c in string.ascii_letters for c in word)
    not_a_variable = '`' not in word
    return contains_letters and not_a_variable


def munge_word(word):
    """ return the lowercase word with trailing/preceding punctuation stripped"""
    word = word.lower()
    if word and word[-1] not in string.ascii_lowercase:
        word = word[:-1]
    if word and word[0] not in string.ascii_lowercase:
        word = word[1:]
    return word


def main():

    counter = Counter()
    word_count = 0

    topdir = sys.argv[1]

    for path in Path(topdir).glob('*.md'):
        with open(path) as blog_post:
            is_code = False
            for line in blog_post:
                if line.startswith('```') or line.startswith('---'):
                    is_code = not is_code
                    continue
                if not is_code:
                    # print(line, end='\n')

                    # now get stats :)
                    for word in line.split():
                        word = word.strip()
                        if is_valid_word(word):
                            word_count += 1
                            munged_word = munge_word(word)
                            counter[munged_word] += 1

    print()
    print('Word Count: ', word_count)
    print()

    # print(counter.most_common(100))
    print("| order | word | count |")
    print("|=======|======|=======|")
    for order, mci in enumerate(counter.most_common(50)):
        word, count = mci
        print(f"| {order + 1} | {word} | {count} |")


if __name__ == "__main__":
    main()
```
