
-- no 1
SELECT price
FROM olist.order_items
ORDER BY price DESC
LIMIT 1;

SELECT price
FROM olist.order_items
ORDER BY price ASC
LIMIT 1;

-- no 2
SELECT 	min(shipping_limit_date) AS start,
		max(shipping_limit_date) AS end
FROM olist.order_items
LIMIT 1;

-- no 3
SELECT customer_state, count(customer_id) as cnt
FROM olist.customers
group by customer_state 
order by cnt desc
LIMIT 3;

-- no 4
SELECT customer_city, 
	count(*) AS cnt_city
FROM olist.customers
WHERE customer_state = 'SP'
GROUP BY customer_city
ORDER BY cnt_city DESC
LIMIT 3;

-- no 5
SELECT COUNT(DISTINCT business_segment) as num
FROM olist.closed_deals
LIMIT 100

-- no 6
SELECT
	business_segment,
	SUM(declared_monthly_revenue) as sum_rev
FROM olist.closed_deals
GROUP BY business_segment
ORDER BY sum_rev DESC 
LIMIT 3;

-- no 7
SELECT
	COUNT(DISTINCT review_score) as cnt_review
FROM olist.order_reviews
LIMIT 3;

-- no 8
SELECT
	*,
    CASE 
    WHEN review_score = 1 THEN "very poor"
    WHEN review_score = 2 THEN "poor"
    WHEN review_score = 3 THEN "average"
    WHEN review_score = 4 THEN "good"    
    ELSE "very good"
    END AS text
FROM olist.order_reviews
LIMIT 100;

-- select 9
SELECT
	review_score,
    COUNT(*) as most    
FROM olist.order_reviews
GROUP BY review_score
ORDER BY most DESC
LIMIT 1;