+++
title = "SQL Schemas from the Terminal with SchemaSpy"
date = 2020-12-20
updated = 2021-01-17
aliases = [ "2020/12/20/SQL-Schemas-from-the-Terminal-with-SchemaSpy.html" ]
+++

I'm building an app backed by MySQL and I need to easily see what its columns are and how they relate to each other so I can write good SQL queries against it. Fortunately, the database geniuses invented the [schema diagram](https://database.guide/what-is-a-database-schema/) for this. I found three or four tools that let me generate a schema diagram from a running database, but the only one I found that could generate diagrams from the terminal is [SchemaSpy](https://github.com/schemaspy/schemaspy). I'm super glad I found it because it also includes other goodies like checking for anomalies - and I can generate this on command by writing a script - no opening an app and typing in login information and clicking apply... just write the script once, run it whenever, see my database in all it's glory.

## Running SchemaSpy

Unfortunately, I had a lot of trouble connecting it to my MySQL database in Azure. Here's how I ended up doing it:

- Install Java 8 - I installed it with `brew install openjdk@8`
- Download the [schemaspy jar file](https://github.com/schemaspy/schemaspy/releases)
- Download the platform independent [MySQL driver](https://dev.mysql.com/downloads/connector/j/8.0.html) and unzip it
- Create a properties file with the contents `serverTimezone=UTC` (otherwise I get timezone errors)
- Run the command

```bash
java \
    -jar ~/Downloads/schemaspy-6.1.0.jar \
    -t mysql \
    -dp ~/Downloads/mysql-connector-java-8.0.22/mysql-connector-java-8.0.22.jar \
    -connprops serverTimezone\\=UTC \
    -host concert-mysqlsrv-dev-weus2.mysql.database.azure.com \
    -port 3306 \
    -s concert_mysql_dev_weus2 \
    -db concert_mysql_dev_weus2 \
    -u concert-user@concert-mysqlsrv-dev-weus2 \
    -p "$TF_VAR_mysql_user_password" \
    -o ./tmpschemaspy/ \
    -vizjs \
```

## Notes

The `-connprops` argument needs two backslashes because I'm in `zsh` where I need to escape a backslash. The `-s` flag refers to `schema` and for MySQL, that's just the database. The `-vizjs` flag means I don't have to install `graphviz`.
