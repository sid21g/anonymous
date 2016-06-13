
SELECT * FROM anon;

SELECT date_entered FROM anon;

SELECT count(*) FROM anon;

SELECT source, count(source) FROM anon GROUP BY source ORDER BY count(source) DESC;

SELECT date_entered, count(date_entered) FROM anon GROUP BY date_entered ORDER BY date_entered DESC;

SELECT link, source, phrase, title, content, date_entered FROM anon ORDER BY date_entered DESC LIMIT 100;

DELETE FROM anon WHERE content NOT LIKE "%<b>%";

CREATE TABLE anon (source, phrase, title, link PRIMARY KEY ON CONFLICT IGNORE, content, date_entered DATE);

SELECT outlets.name FROM anon LEFT OUTER JOIN outlets on anon.source = outlets.url;

SELECT anon.source, outlets.name, anon.phrase, anon.title, anon.link, anon.content, anon.date_entered FROM anon LEFT OUTER JOIN outlets ON anon.source = outlets.url;

SELECT outlets.name, outlets.url FROM outlets ORDER BY outlets.name;

SELECT DISTINCT anon.source, outlets.name FROM anon JOIN outlets ON anon.source = outlets.url ORDER BY outlets.name;

SELECT DISTINCT anon.source FROM anon;

SELECT anon.title, count(anon.title) FROM anon GROUP BY anon.title ORDER BY count(anon.title) DESC;

SELECT anon.source, anon.content, count(anon.content) FROM anon GROUP BY anon.content ORDER BY count(anon.content) DESC;

DELETE FROM anon WHERE ROWID NOT IN (SELECT min(ROWID) FROM anon GROUP BY content);

SELECT min(ROWID) FROM anon GROUP BY source, content;