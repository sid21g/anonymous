
SELECT * FROM anon;

SELECT date_entered FROM anon;

SELECT count(*) FROM anon;

SELECT source, count(source) FROM anon GROUP BY source ORDER BY count(source) DESC;

SELECT date_entered, count(date_entered) FROM anon GROUP BY date_entered ORDER BY date_entered DESC;

SELECT link, source, phrase, title, content, date_entered FROM anon ORDER BY date_entered DESC LIMIT 100;

CREATE TABLE [anon] (
  [source]  NULL
, [phrase]  NULL
, [title]  NULL
, [link]  NOT NULL
, [content]  NULL
, [date_entered] date NULL
, CONSTRAINT [sqlite_autoindex_anon_1] PRIMARY KEY ([link])
);

