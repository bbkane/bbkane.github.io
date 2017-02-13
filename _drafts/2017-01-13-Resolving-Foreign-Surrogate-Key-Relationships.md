---
layout: default
title: Resolving Foreign Surrogate Key Relationships
---

I've been designing a database recently with surrogate keys and I've had trouble
matching the foreign key from one table into the other while inputting data. I
wanted to note two ways to resolve it- one more on the Python side, one more on
the SQL side.

# The schema

I've thought of a simple schema to illustrate this problem (in SQLite3 syntax)

```sql
CREATE TABLE cupboard
(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE mug
(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    FOREIGN KEY (cupboard_id) REFERENCES cupboard(id)
);
```

As you can see, I'm using unique constraints to keep the right things unique,
but I'm generating a surrogate primary key called `id`. In this example, the
`name`s would be perfectly good primary keys, but in non-toy examples I find
`id` generally works better. For example, using a unique constraint over multiple columns is
easier than having a composite primary key that also needs to be foreign key.
This can be a nuanced subject however, and experts seem to disagree. TODO: get
reading material.

One disadvantage to using surrogate keys as primary/foreign keys is how to insert a data stream into
tables. Imagine a data stream that looks like this:

```
cupboard_name, mug_name
cupboard_name, mug_name
...
```

What's the best way to insert that into our table? Obviously the name fields can
be easily inserted, but what about the `id` and `chassis_id` fields? Those
aren't a natural property of the data, but of the database. I have two
approaches to doing this in Python and SQL- one is more Python heavy and it uses a
"insert cupboard, select cupboard.id, insert mug" approach and the other one
relies more on SQL and uses a "insert cupboard, mug into staging table, insert
into final tables, resolve foreign keys" approach. One thing to note in both
approaches is that I might be parsing and inserting the same data twice. I use
the `OR IGNORE` clause in the insert statement to utilize my `UNIQUE` columns
and not insert the same data twice - see
[this answer on StackOverflow](http://stackoverflow.com/a/12105319/2958070).

TODO: move more of the algorithm into the first paragraph- but the problem isn't
fully explained until here.

# Python Heavy Approach

This approach has the benefit that it's probably more efficient and it's the
obvious approach, but it has the disadvantage that it involves a two way
communication with the database instead of inserting only and depending on your
language preference, it requires more code as well.

The first thing to do is to write a function to insert a record and get the id-
I make this generic by using a dictionary for the fields:

TODO: fix this code

```python
from itertools import repeat
import sqlite3

def insert_and_get_id(conn, cur, table, fields):
    # implement
```

I can use this approach to turn that input stream into tables in the following
manner:

```python
with contextlib.closing(sqlite3.connect('db-name.sqlite3')) as conn:
    cur = conn.cursor()
    for cupboard_name, mug_name in input_stream:
        cupboard_id = insert_and_get_id(conn, cur, 'cupboard', dict(name=cupboard_name))
        insert_and_get_id(conn, cur, 'mug', dict(name=mug_name, cupboard_id=cupboard_id))
```

I've safely abstracted the communication with the database, and this might be a
decent way to do it.

TODO: enumerate advantages and disadvantages

# The SQL heavy approach

TODO: test this whole fucking thing

The SQL approach is to use a staging table to capture the data as soon as
possible and then to resolve the relationships with more SQL.

First create a staging table:

```sql
CREATE cupboard_mug_staging
(
    cupboard_name TEXT,
    mug_name TEXT,
    PRIMARY KEY (cupboard_name, mug_name)
)
```

This table, unlike my final ones, does have a composite "natural" primary key.
This means I can use my little `INSERT OR IGNORE` trick to not duplicate data
when I insert.

Then insert the data into the staging table:

```
with contextlib.closing(sqlite3.connect('db-name.sqlite3')) as conn:
    cur = conn.cursor()
    # insert the data into the staging table
    for cupboard_name, mug_name in input_stream:
        cur.execute('INSERT OR IGNORE INTO cupboard_mug_staging (cupboard_name, mug_name) FIELDS (?,?)', (cupboard_name, mug_name))
    # input stream exausted. Time for pure table munging

    staging_table_data = cur.execute('SELECT cupbard_name, mug_name FROM cupboard_mug_staging')
    staging_table_data = staging_table_data.fetchall()
    for cupboard_name, mug_name in staging_table_data:
        cur.execute('INSERT OR IGNORE INTO cupbard (name) VALUES (?)', (cupboard_name,))
        cur.execute('INSERT OR IGNORE INTO mug (name, cupboard_id) VALUES
        (?, (SELECT id FROM cupboard WHERE cupboard.name = ?))', (mug_name,
        cupboard_name)
```

I don't even need a staging table with that approach! Forget about it and a
couple of other loops! The only thing I might need is to cache the result.

This is less general
