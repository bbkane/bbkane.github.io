---
layout: default
title: SQLite3 Snippets
---

# `~/.sqliterc` customizations

The default `sqlite3` shell can read from a dotfile! [Here](https://github.com/bbkane/dotfiles/tree/master/sqlite3) are some nice customizations for it

This file can reloaded into the shell with the command `.read <filename>`. This `.read` command is also useful for reading sql scripts.

# Simple table example

Cause I forget the syntax every once in a while :)


```sql

DROP TABLE my_table;

CREATE TABLE my_table
(
    my_variable INT,
    my_other VARCHAR(20)
);

INSERT INTO my_table VALUES (1, 'one');
INSERT INTO my_table VALUES (2, 'two');

SELECT * FROM my_table;
```

### Find duplicate columns in a table

I want to write somewhere an easy inner join to find records with duplicate
columns.

```sql
SELECT mt1.name 
FROM 
    my_table AS mt1
    JOIN my_table as mt2 ON mt1.name = mt2.name AND mt1.id != mt2.id
```

# See contents of a table

From [StackOverflow](https://stackoverflow.com/a/7679086/2958070):

```
PRAGMA table_info([tablename]);
```
