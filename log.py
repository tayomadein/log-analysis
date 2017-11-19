#!/usr/bin/env python3
#
# "Database code" for Log Analysis Project.

import psycopg2

DBNAME = "news"


def querydb(query):
    """
    querydb() takes an SQL query as a parameter, 
    executes the query and returns the results as a list of tuples.
    args:
       query - (string) an SQL query statement to be executed.

    returns:
       A list of tuples containing the results of the query.
    """

    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results
    except psycopg2.Error as e:
        print ("Database error occured\n", e)


def get_top_articles():
    """Return the top 3 most view articles."""

    query = """
        select title, views
        from (
            select path, count (*) as views
            from log
            where path like '%article%'
            and log.status like '%OK%'
            group by path) as topthree, articles
        where topthree.path = '/article/' || articles.slug
        order by views desc
        limit 3
    """

    return querydb(query)


def get_popular_authors():
    """Return all authors in order of popularity."""

    query = """
        select name, allviews.views as author_views
        from (
            select author, count (articles.title) as views
            from log, articles
            where log.path = concat('/article/', articles.slug)
            group by author) as allviews, authors
        where allviews.author = authors.id
        order by author_views desc
    """

    return querydb(query)


def get_error_rate():
    """Return days were more than 1% of requests lead to errors."""

    query = """
        select to_char(output.date, 'FMMonth FMDD, YYYY'),
            round((output.error*100.00/output.total), 1) as perc
        from (
            select response.date, errortable.error, response.total
            from (
                select date(time) as date, count (*) as error
                from log
                where status not like '%OK%'
                group by date) as errortable,
                (select date(time) as date, count (*) as total
                from log
                group by date) as response
            where errortable.date = response.date
            group by response.date, errortable.error, response.total) as output
        where (output.error*100.00/output.total) > 1.0
    """
    return querydb(query)


def print_output():
    """Print Query results to a text file"""

    print ("Getting Log Analysis")

    f = open("output.txt", "w")
    f.write("Logs Analysis:\n")

    dboutput = get_top_articles()
    f.write("\n1. Most Popular Articles:\n")
    for title, views in dboutput:
        entry = '{} - {} views\n'.format(title, views)
        f.write(entry)

    dboutput = get_popular_authors()
    f.write("\n\n2. Most Popular Authors:\n")
    for title, views in dboutput:
        entry = '{} - {} views\n'.format(title, views)
        f.write(entry)

    dboutput = get_error_rate()
    f.write("\n\n3. More than 1% of requests led to errors on:\n")
    for date, perc in dboutput:
        entry = '{} - {}% requests\n'.format(date, perc)
        f.write(entry)

    f.close()

if __name__ == '__main__':
    print_output()
