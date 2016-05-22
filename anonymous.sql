
SELECT * FROM anon;

SELECT date_entered FROM anon;

SELECT count(*) FROM anon;

SELECT source, count(source) FROM anon GROUP BY source ORDER BY count(source) DESC;

SELECT date_entered, count(date_entered) FROM anon GROUP BY date_entered ORDER BY count(date_entered) DESC;

SELECT * FROM anon WHERE date_entered = '2016-05-21';

CREATE TABLE [anon] (
  [source]  NULL
, [phrase]  NULL
, [title]  NULL
, [link]  NOT NULL
, [content]  NULL
, [date_entered] date NULL
, CONSTRAINT [sqlite_autoindex_anon_1] PRIMARY KEY ([link])
);

