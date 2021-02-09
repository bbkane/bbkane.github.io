+++
title = "Learn SQL"
date = 2017-10-10
updated = 2019-03-26
aliases = [ "2017/10/10/Learn-SQL.html" ]
+++

SQL is one of the best benefit/cost skills to learn. It's fairly easy to learn,
and it immediately becomes useful for many jobs- including software
engineering, accounting, law, or any other job that deals with data.

## Learn SQL

I recommend the following links to learn SQL. To be completely honest, I
haven't tried all of them, but they look decent and they're free.

SQL (and other relational databases) are basically working with the math
concept of *sets*. It's much easier to learn SQL if you're somewhat familiar
with sets. Unfortunately, I couldn't find a good resource for learning set
algebra, but if you just want a refresher, you can try the quizzes at
[hackerrank](https://www.hackerrank.com/domains/databases/relational-algebra).
If you don't know anything about set algebra, don't get hung up on it- you'll
learn a lot of it through the following links.

For actually learning SQL, if you enjoy learning from videos, I recommend [Khan
Academy](https://www.khanacademy.org/computing/computer-programming/sql#sql-basics).
If you'd rather read to learn, I recommend
[SQLCourse](http://www.sqlcourse.com/). Both of these sites include exercises
you can run without installing anything!

Once you want to practice SQL, head to
[hackerrank](https://www.hackerrank.com/domains/sql/select) to solve some
challenges or [Franchise](https://franchise.cloud/) to play with it in your browser
on sample datasets!

## Work with SQL

Eventually you will want to create, play with, and use your own databases. I
recommend starting with SQLite. Once you get used to databaseses more, look
into MariaDB or Postgres - in my experience, MariaDB has better tooling, and
Postgres has more features and fewer odd design decisions.

### SQLite


SQLite might be the most used code in the world- every copy of
Windows 10 uses SQLite in the operating system, Firefox uses it to store
bookmarks, and every Android and iPhone has it. NASA is actually running SQLite
in space. Learning SQLite can be super valuable.

I recommend starting with [SQLite](https://www.sqlite.org/) and [DB Browser for
SQLite](http://sqlitebrowser.org/). These tools are both easy to install and
uninstall and each database you create is just a file so you can email it
between computers or copy it before trying something risky with your database.

Alternatively (thank you [@hautdefrance](https://github.com/hautdefrance)!), you can play with SQLite
completely online, in a website! Check out
[Franchise](https://franchise.cloud/), [SQLite
Browser](https://extendsclass.com/sqlite-browser.html), or [SQLite
Online](https://sqliteonline.com).

### MySQL (MariaDB)

Many web apps use MySQL (or its clone MariaDB). It's a tad more complicated to
set up than SQLite, but not too bad. I recommend installing
[MariaDB](https://mariadb.org/) and [MySQL
Workbench](https://www.mysql.com/products/workbench/).

Note that whichever SQL vendor (SQLite, MySQL, Postgres, or whoever else) you
use will provide a somewhat different version of SQL, but for basic queries
they're pretty identical, and learning one makes the others very familiar too.
