+++
title = "Quick Python Diff"
date = 2016-06-13
updated = 2016-12-25
aliases = [ "2016/06/13/Quick-Python-Diff.html" ]
+++

If you need a quick, cross-platform diff between files that makes a nice
HTML document for your perusal, Python has your back:


```python
import difflib

first_name = 'firstname.txt'
second_name = 'secondname.txt'
diff_name = 'diff.html'

with open(first_name, 'r', encoding='utf_8') as first:
    fromlines = first.readlines()

with open(second_name, 'r', encoding='utf_8') as second:
    tolines = second.readlines()

with open(diff_name, 'w', encoding='utf_8') as output:
    output.write(difflib.HtmlDiff().make_file(fromlines, tolines,
                                              first_name, second_name))
```

If you need more functionality, check out `vimdiff`, a more featureful version of this script at the [python docs](https://docs.python.org/3.5/library/difflib.html#a-command-line-interface-to-difflib), and the linux tools `diff` and `sdiff`.
