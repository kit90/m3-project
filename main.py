#!/usr/bin/env python3

import psycopg2


def execute_select_query(c, query):
    c.execute(query)
    colnames = [desc[0] for desc in c.description]
    rows = c.fetchall()
    return colnames, rows


def print_resultset(colnames, rows):
    for colname in colnames:
        print(colname, end='\t|')
    print()

    for _ in range(len(colnames)):
        print('----', end='\t|')
    print()

    for row in rows:
        for cell in row:
            print(str(cell), end='\t|')
        print()

    print()


if __name__ == '__main__':
    db = psycopg2.connect(database='news')
    c = db.cursor()

    print('1. What are the most popular three articles of all time?')

    query1 = '''
    select title, count(*) as num
      from articles, log_slugs
      where articles.slug = log_slugs.slug
      group by title
      order by num desc
      limit 3;
    '''

    colnames1, rows1 = execute_select_query(c, query1)
    print_resultset(colnames1, rows1)

    print('2. Who are the most popular article authors of all time?')

    query2 = '''
    select name, count(*) as num
      from authors, articles, log_slugs
      where authors.id = articles.author and articles.slug = log_slugs.slug
      group by name
      order by num desc;
    '''

    colnames2, rows2 = execute_select_query(c, query2)
    print_resultset(colnames2, rows2)

    print('3. On which days did more than 1% of requests lead to errors?')

    query3 = '''
    select *
      from date_percent_error
      where percent_error > 1;
    '''

    colnames3, rows3 = execute_select_query(c, query3)
    print_resultset(colnames3, rows3)

    c.close()
    db.close()
