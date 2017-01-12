---
layout: default
title: SQLite3 Conveniences
---

Using the `sqlite3` command prompt is a pain on my linux box.
For some reason, the standard keyboard shortcuts don't work over SSH, so I can't
backspace, get previous commands, or use other basic shell manipulation commands.

Instead, it's easier to create a file and read its commands to work for me.
This also lets me set a few options I like, run multiple commands easily, and get
syntax highligting in the editor.

```sql
-- show the command entered
.echo on
-- show the column names
.headers on
-- get nice columns instead of the default '|' separated field
.mode column

SELECT * FROM my_table WHERE my_variable = 1;

-- ... and so on
```

This file can loaded into the shell with the command `.read <filename>`.

For example:

#### commands.sql

```sql
.echo on
.headers on
.mode column

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

#### sqlite3 shell

```sql
sqlite> .read commands.sql
.read commands.sql
.echo on
.headers on
.mode column

DROP TABLE my_table;

CREATE TABLE my_table
(
    my_variable INT,
    my_other VARCHAR(20)
);

INSERT INTO my_table VALUES (1, 'one');
INSERT INTO my_table VALUES (2, 'two');

SELECT * FROM my_table;
my_variable  my_other
-----------  ----------
1            one
2            two

sqlite>
```

Like the nice table at the bottom with column lables and nicely separated fields?
I do too.

### Errata

I want to write somewhere an easy inner join to find records with duplicate
columns. It doesn't really fit into this post, so here it is on the bottom.

```sql
SELECT mt1.name 
FROM 
    my_table AS mt1
    JOIN my_table as mt2 ON mt1.name = mt2.name AND mt1.id != mt2.id
```
