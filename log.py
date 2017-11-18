#!/usr/bin/env python3
#
# "Database code" for Log Analysis Project.

import psycopg2

DBNAME = "news"


def querydb(query):
    """Handle all db queries"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    return c.fetchall()
    db.close()


def get_top_articles():
    """Return the top 3 most view articles."""

    query = """
        select title, views
        from (
            select path, count (*) as views
            from log
            where path like '%article%'
            group by path) as topthree, articles
            where topthree.path like '%' || articles.slug || '%'
            order by views desc
            limit 3
    """

    return querydb(query)


def get_popular_authors():
    """Return all authors in order of popularity."""

    query = """
        select name, sum(views) as author_views
        from (
            select title, author, count (articles.title) as views
            from log, articles
            where log.path like '%' || articles.slug || '%'
            group by title, author) as allviews, authors
            where allviews.author = authors.id
            group by name
            order by author_views desc
    """

    return querydb(query)


def get_error_rate():
    """Return days were more than 1% of requests lead to errors."""

    query = """
        select output.date,
            round((output.error*100.00/output.total), 1) as perc
        from (
            select response.date, errortable.error, response.total
            from (
                select to_char(time, 'YYYY-MM-DD') as date, count (*) as error
                from log
                where status not like '%OK%'
                group by date) as errortable,
                (select to_char(time, 'YYYY-MM-DD') as date, count (*) as total
                from log
                group by date) as response
            where errortable.date = response.date
            group by response.date, errortable.error, response.total) as output
        where (output.error*100.00/output.total) > 1.0;
    """
    return querydb(query)


def print_output():
    """Print Query results to a text file"""

    print ("Getting Log Analysis")

    f = open("output.txt", "w")
    f.write("Logs Analysis:\n")

    dboutput = get_top_articles()
    f.write("\n1. Most Popular Articles:\n")
    for row in dboutput:
        entry = row[0] + ' - ' + str(row[1]) + " views\n"
        f.write(entry)

    dboutput = get_popular_authors()
    f.write("\n\n2. Most Popular Authors:\n")
    for row in dboutput:
        entry = row[0] + ' - ' + str(row[1]) + " views\n"
        f.write(entry)

    dboutput = get_error_rate()
    f.write("\n\n3. More than 1% of requests led to errors on:\n")
    for row in dboutput:
        entry = row[0] + ' - ' + str(row[1]) + "% requests\n"
        f.write(entry)

    f.close()

print_output()
