#!/usr/bin/env python3
#
# "Database code" for Log Analysis Project.

import psycopg2

DBNAME = "news"

def get_top_articles():
  """Return the top 3 most view articles."""

  query = """
    select title, views
    from (
        select path, count (*) as views
        from log
        where path like '%article%'
        group by path
        order by views desc
        limit 3) as topthree, articles
        where topthree.path like '%' || articles.slug || '%'
  """

  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(query)
  return c.fetchall()
  db.close()

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

  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute(query)
  return c.fetchall()
  db.close()



dboutput = get_popular_authors()
# get_top_articles()
print dboutput
