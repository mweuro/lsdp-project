SELECT title, score
FROM submissions
WHERE created_utc >= now() - interval '1 day'
ORDER BY score ASC
LIMIT 10;