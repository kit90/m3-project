create view log_slugs as
  select substring(path from '^/article/(.+)') as slug
  from log;

select title, count(*) as num
  from articles, log_slugs
  where articles.slug = log_slugs.slug
  group by title
  order by num desc
  limit 3;

select name, count(*) as num
  from authors, articles, log_slugs
  where authors.id = articles.author and articles.slug = log_slugs.slug
  group by name
  order by num desc;

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

select *
  from date_percent_error
  where percent_error > 1;
