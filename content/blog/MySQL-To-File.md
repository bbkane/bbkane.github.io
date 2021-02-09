+++
title = "MySQL To File"
date = 2016-06-06
updated = 2016-12-25
aliases = [ "2016/06/06/MySQL-To-File.html" ]
+++

# How To Use a MySQL command on the BASH command line

If you want to print the output from the SQL commands in one file to another, use:

```bash
mysql -u <username> --password='<password>' <database_name> -vvv < <path/to/file_with_commands> > <path/to/output_file>
```

The `-vvv` is the verboseness of the command and is optional,
the `<` is a redirection from a file, and the `>` redirects from stdout to another file.

For example:

```bash
mysql -u bkane --password='im_totes_secure' books_db -vvv < ./work.mysql > ./output.txt
```

prints the commands in `work.mysql` to `output.txt`. If you just want the output to the terminal, leave off the `> <path/to/output_file>`.


This is the easiest way. *Note that using the bare password on the command line is
[insecure](http://unix.stackexchange.com/questions/78734/why-shouldnt-someone-use-passwords-in-the-command-line).*
You probably shouldn't use this at work.

If you're only want to see one command, it's probably easier to use process substitution:

```bash
mysql -u bkane --password='im_totes_secure' books_db -vvv < <( echo 'SELECT * FROM books') > ./output.txt
```
