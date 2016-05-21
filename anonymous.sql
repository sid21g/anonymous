
SELECT * FROM anon;

SELECT count(*) FROM anon;

SELECT source, count(source) FROM anon GROUP BY source ORDER BY count(source) DESC;

