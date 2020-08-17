-- no 1
SELECT
client_id
FROM bank.client
WHERE district_id = 1
LIMIT 5;

-- no 2
SELECT
client_id
FROM bank.client
WHERE district_id = 72
ORDER BY client_id DESC
LIMIT 1;

-- no 3
SELECT 
amount
FROM bank.loan
ORDER BY amount
LIMIT 3;

-- no 4
SELECT DISTINCT
status
FROM bank.loan
ORDER BY status ASC;

-- no 5
SELECT 
loan_id
FROM bank.loan
ORDER BY payments DESC
LIMIT 1;

-- no 6
SELECT 
account_id, 
amount
FROM bank.loan
ORDER BY account_id ASC
LIMIT 5;

-- no 7
SELECT 
account_id
FROM bank.loan
WHERE duration = 60
ORDER BY amount ASC
LIMIT 5;

-- no 8
SELECT DISTINCT
k_symbol
FROM bank.`order`;

-- no 9
SELECT 
order_id
FROM bank.`order`
WHERE account_id = 34;

-- no 10
SELECT DISTINCT
account_id
FROM bank.`order`
WHERE order_id BETWEEN 29540 AND 29560;

-- no 11
SELECT 
amount
FROM bank.`order`
WHERE account_to = 30067122;

-- no 12
SELECT 
trans_id, 
`date`, 
`type`, 
amount
FROM bank.trans
WHERE account_id = 793
ORDER BY date DESC
LIMIT 10;