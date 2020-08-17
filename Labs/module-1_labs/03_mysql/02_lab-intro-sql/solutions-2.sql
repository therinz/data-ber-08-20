-- no 1
SELECT
MIN(DATE(first_contact_date)),
max(DATE(first_contact_date))
FROM olist.marketing_qualified_leads

-- no 2
SELECT
origin,
count(*) as COUNT
FROM olist.marketing_qualified_leads
WHERE YEAR(first_contact_date) = 2018
GROUP BY origin
ORDER BY COUNT DESC
LIMIT 3;

-- no 3
SELECT
first_contact_date,
COUNT(mql_id) as COUNT
FROM olist.marketing_qualified_leads
GROUP BY DATE(first_contact_date)
ORDER BY COUNT DESC
LIMIT 1;

-- no 4
SELECT
product_category_name,
COUNT(*) as COUNT
FROM olist.products
GROUP BY product_category_name
ORDER BY COUNT DESC
LIMIT 2;

-- no 5
SELECT
product_category_name,
MAX(product_weight_g) as maxi
FROM olist.products
GROUP BY product_weight_g
ORDER BY maxi DESC
LIMIT 1;

-- no 6
SELECT
product_category_name,
product_length_cm + product_height_cm + product_width_cm as dimension
FROM olist.products
GROUP BY dimension
ORDER BY dimension DESC
LIMIT 1;

-- no 7
SELECT
payment_type,
COUNT(*) as COUNT
FROM olist.order_payments
GROUP BY payment_type
ORDER BY COUNT DESC
LIMIT 1;

-- no 8
SELECT
MAX(payment_value)
FROM olist.order_payments
LIMIT 1;

-- no 9
SELECT
seller_state,
COUNT(DISTINCT seller_city) as COUNT
FROM olist.sellers
GROUP BY seller_state
ORDER BY COUNT DESC
LIMIT 3;