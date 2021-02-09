+++
title = "Path Name Conventions"
date = 2017-05-03
updated = 2017-05-03
aliases = [ "2017/05/03/Path-Name-Conventions.html" ]
+++

I recently did some BASH scripting that dealt a lot with paths.
I want to record here for posterity the conventions I used to keep things
straight, copied straight from the code.

```bash
# Naming Conventions
# Because this script deals heavily with moving files, I've established some
# conventions for dealing with them
#
# <variable>_path is the full path from / to a file <variable>
# Example:
#   boot_log_path might be the name for "/var/log/boot.log"
#
# <variable>_dir is the full path from / to the directory containing <variable>
# <variable>_dir does not end in a '/'
# Example:
#  boot_log_dir is the name for "/var/log"
#
# <variable>_name is the name of the file itself
# Example:
#  boot_log_name is the name for "boot.log"
#
# Consequences:
#  basename "${<variable>_path}" == "${<variable>_name}"
#  "${<variable>_path}" == "${<variable>_dir}/${<variable>_name}"
#
# Examples:
#  basename "${boot_log_path}" == "${boot_log_name}"
#  basename "/var/log/boot.log" == "boot.log"
#
#  "${boot_log_path}" == "${boot_log_dir}/${boot_log_name}"
#  "/var/log/boot.log" == "/var/log/boot.log"
```


