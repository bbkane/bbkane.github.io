+++
title = "Removing Passwords from a Git Repo"
date = 2016-09-19
updated = 2016-12-26
aliases = [ "2016/09/19/Removing-Passwords-from-a-Git-Repo.html" ]
+++

When googling how to remove passwords from a git repository,
I found [this very helpful link](http://www.davidverhasselt.com/git-how-to-remove-your-password-from-a-repository/).

It was so helpful, I turned it into the following Python script:

```python
import shutil
import subprocess as sp
import sys


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 %s first_word second_word" % sys.argv[0], file=sys.stderr)
        raise SystemExit("Use the correct arguments")
    first_word = sys.argv[1]
    second_word = sys.argv[2]

    if sys.platform == "linux" or sys.platform == "linux2":
        if shutil.which('sed'):
            sed_program = 'sed'
        else:
            raise SystemExit("Install sed")
    elif sys.platform == "darwin":
        if shutil.which('gsed'):
            sed_program = 'gsed'
        else:
            # Note, can change the command and not need gsed
            raise SystemExit("Install gsed.")
    else:
        raise SystemExit("Platform not supported")

    {% comment %}Need to escape the double quotes below {% endcomment %}
    {% raw %}
    find_str = r"find . -type f -exec {sed_program} -i -e 's/{first_word}/{second_word}/g' {{}} \;"
    {% endraw %}
    find_str = find_str.format(sed_program=sed_program,
                               first_word=first_word,
                               second_word=second_word)
    command = ['git', 'filter-branch', '--tree-filter', find_str]

    response = input("Is '{command}' okay (yes)?".format(command=command))
    if response == 'yes':
        sp.run(command)
    else:
        print("cancelling...")

if __name__ == '__main__':
    main()
```
