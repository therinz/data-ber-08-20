-- 04_lab-sql-aggregations/lab-2-sql-aggregations.md

-- no 1
SELECT district_id, COUNT(client_id)
FROM bank.client
WHERE district_id < 10
GROUP BY district_id
ORDER BY district_id ASC;

-- no 2
SELECT type, COUNT(card_id) as c
FROM bank.card
GROUP BY type
ORDER BY c DESC;

-- no 3
SELECT account_id, 
SUM(amount) AS s
FROM bank.loan
GROUP BY account_id
ORDER BY s DESC
LIMIT 10;

-- no 4
SELECT `date`, COUNT(loan_id)
FROM bank.loan
WHERE `date` < 930907
GROUP BY `date`
ORDER BY `date` DESC
LIMIT 5;

-- no 5
SELECT `date` as d,
duration,
COUNT(loan_id)
FROM bank.loan
WHERE `date` BETWEEN 971201 AND 971231
GROUP BY `date`, duration
ORDER BY d, duration ASC;

-- no 6
SELECT account_id,
`type` AS t,
SUM(amount) AS total_amount
FROM bank.trans
WHERE account_id = 396
GROUP BY `type`
ORDER BY `type` ASC;

-- no 7
SELECT account_id,
CASE WHEN `type` = 'PRIJEM' 
THEN 'INCOMING' 
ELSE 'OUTGOING' 
END AS transaction_type,
FLOOR(SUM(amount)) AS total_amount
FROM bank.trans
WHERE account_id = 396
GROUP BY `type`
ORDER BY `type` ASC;

-- no 8
SELECT account_id,
FLOOR(SUM(IF(`type` = 'PRIJEM', amount, 0))) AS incoming,
FLOOR(SUM(IF(`type` = 'VYDAJ', amount, 0))) AS outgoing,
FLOOR(SUM(IF(`type` = 'PRIJEM', amount, 0))) - FLOOR(SUM(IF(`type` = 'VYDAJ', amount, 0))) AS difference
FROM bank.trans
WHERE account_id = 396;

-- no 9
SELECT account_id,
FLOOR(SUM(IF(`type` = 'PRIJEM', amount, 0))) - FLOOR(SUM(IF(`type` = 'VYDAJ', amount, 0))) AS difference
FROM bank.trans
GROUP BY account_id
ORDER BY difference DESC
LIMIT 10;
