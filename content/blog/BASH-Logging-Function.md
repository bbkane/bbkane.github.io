+++
title = "BASH Logging Function"
date = 2016-09-09
updated = 2016-12-25
aliases = [ "2016/09/09/BASH-Logging-Function.html" ]
+++

This is a small BASH logging function to record the output of a command:

```bash
function logit {
    today=$(date +%Y-%m-%d.%H.%M)
    "$@" > >(tee "$1".stdout."$today".log) 2> >(tee "$1".stderr."$today".log >&2)
}
```

How it works:

1. The output of the `date` command is stored in `$today`
1. All arguments to the function ( `$@` ) are executed
and stdout and stderr are redirected to files.
    1. `>` redirects `stdout` and `2>` redirects `stderr`
    1. `>( )` is a `process substitution` construction.
    The `>` in front means that the input passed to the subprocess will be treaded as `stdin`.
    1. That `stdin` is redirected to a file by `tee`.
