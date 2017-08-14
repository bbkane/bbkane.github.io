from collections import Counter
from pathlib import Path
import string

# This script goes through my _posts directory, strips
# out lines surrounded by ``` or --- blocks, then does a little
# statistics on the results


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

    for path in Path('.').glob('*.md'):
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
                        word_count += 1
                        counter[munge_word(word)] += 1

    # print(counter.most_common(100))
    print(counter)
    print('word_count: ', word_count)


if __name__ == "__main__":
    main()

