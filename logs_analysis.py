#!/usr/bin/env python3

'''This program is a reporting tool that prints reports in plain text 
based on the fetched data from the database.This is a Python program 
that use psycopg2 modul to connect to the database'''

import psycopg2
from datetime import datetime

what_top_articles = '\nThe most popular three articles of all time:\n'

top_articles_query = '''
SELECT articles.title, 
Count(path) AS num_views 
FROM   articles 
LEFT JOIN log 
ON Concat('/article/', articles.slug) = log.path 
GROUP  BY log.path, 
articles.title 
ORDER  BY num_views DESC 
LIMIT  3;'''

what_top_authors = "\nThe most popular article authors of all time:\n"

top_authors_query = '''
SELECT NAME, 
Count(path) AS num_views 
FROM   authors 
RIGHT JOIN article_owner 
ON authors.id = article_owner.id 
GROUP  BY authors.NAME 
ORDER  BY num_views DESC;'''

what_days_error = "\nDays on which more than 1 % of requests lead to errors:\n"


days_error_over_one = '''
SELECT day, 
Round(percent, 2) AS percent 
FROM   error_percentage 
WHERE  percent > 1; '''



# connect to DB an fetch data

def get_reports(query):
    '''connect to DB and return all data requested by the query'''    
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    reports = c.fetchall()
    db.close()
    return reports
    
# print result of the first two queries

def print_reports(query,question):
    '''print a formated result of the query'''   
    print(question)
    data = get_reports(query)
    for i in range(len(data)):
        message = "\t{} -- {} views.".format(data[i][0], data[i][1])
        print(message)
    print('')

# print result of the last query

def print_error_report(query, question):
    '''print a formated result of the query, and change date format'''
    print(question)
    data = get_reports(query)
    for i in range(len(data)):
        date_format = data[i][0].strftime('%B %d, %Y')
        message="\t{} -- {}% errors.".format(date_format, data[i][1])
        print(message)
    print('')
    
if __name__ == "__main__":

    try:
        print_reports(top_articles_query, what_top_articles)
        print_reports(top_authors_query, what_top_authors)
        print_error_report(days_error_over_one, what_days_error)
		
    except psycopg2.OperationalError:
        print("\ncan't connect to the database, make sure the database exists.\n")
    
