# Logs Analysis Project 
**(Full Stack Web Developer Nanodegree Program)**

## Description
In this project, the task is creating a reporting tool that prints out reports (in plain text) based on the data fetched from the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

## Questions
The student must write queries to fetch data requested by the questions below:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements
* [Python 3](https://www.python.org/downloads/)
* [Vagrant 2](https://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Git](https://git-scm.com/downloads)

## How to run the program?
Flollow the steps below:

**Preparation**
1. Download and install all requirements from the links above.
2. Download this [folder](https://s3.amazonaws.com/video.udacity-data.com/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip) with preconfigured vagrant settings, and then `cd` in `/vagrant`, after that run `vagrant up` then `vagrant ssh`
3. Download [this data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), and then unzip it and put it into the vagrant directory, which is shared with your virtual machine, in the folder you have been download from the step 2.
4. Download the `logs_analysis.py` and put it in the same folder where you put the data just above.

**Running**
1. Open the terminal and make sure you are in the vagrant directory, and then run `psql -d news -f newsdata.sql` Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
2. Now you are connected to the news database, so run the following SQL code, in order to add some views to your database
Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
3.Now you are connected to the news database, so run the following SQL code, to add some views to your database:
```SQL
CREATE VIEW article_owner 
AS 
  SELECT articles.author AS id, 
         articles.title, 
         log.path 
  FROM   articles 
         left join log 
                ON Concat('/article/', articles.slug) = log.path 
  ORDER  BY log.path, 
            articles.title; 
```
```SQL
CREATE VIEW good_response 
AS 
  SELECT Date(time) AS day, 
         Count(*)   AS good 
  FROM   log 
  WHERE  status LIKE '200%' 
  GROUP  BY day; 
```
```SQL
CREATE VIEW bad_response 
AS 
  SELECT Date(time) AS day, 
         Count(*)   AS error 
  FROM   log 
  WHERE  status LIKE '404%' 
  GROUP  BY day; 
  ```
  ```SQL
CREATE VIEW error_percentage
AS
  SELECT a.day,
         ( b.error * 100.0 / (b.error + a.good)) AS percent
  FROM   good_response AS a
         INNER JOIN bad_response AS b
                 ON a.day = b.day; 
  ```
3. Now exit the database by typing `\q` then ENTER, and run the `python logs_analysis.py`, you should have the same results as in the `output.txt`.
  





