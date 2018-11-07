# Logs Analysis
## Overview
This is a reporting tool that prints out reports (in plain text) based on the data in the `news` database. This 
reporting tool is a Python program using the `psycopg2` module to connect to the database. It answers the following 
questions.
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The following views should be present for the program to work.
```postgresql
create view log_slugs as
  select substring(path from '^/article/(.+)') as slug
  from log;

create view dates_with_status as
  select time::date as date, status
  from log;

create view date_num_status as
  select date, count(status) as num_status
  from dates_with_status
  group by date;

create view date_num_status_error as
  select date, count(status) as num_status_error
  from dates_with_status
  where status <> '200 OK'
  group by date;

create view date_percent_error as
  select date_num_status.date, num_status_error::float / num_status * 100 as percent_error
  from date_num_status, date_num_status_error
  where date_num_status.date = date_num_status_error.date;
```
## Requirements
- Python (3.5+)
## Installation
```bash
pip3 install -r requirements.txt
```
## Usage
```bash
python3 main.py
```
A sample output is given in `output.txt`.
## License
This program is available under the MIT License.
