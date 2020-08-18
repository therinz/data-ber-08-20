-- data-ber-08-20/Labs/module-1_labs/03_mysql/05_lab-mysql-select/

-- Challenge 1
SELECT 
a.au_id 			as `AUTHOR ID`,
a.au_lname 			as `LAST NAME`,
a.au_fname 			as `FIRST NAME`,
t.title 			as `TITLE`,
p.pub_name 			as `PUBLISHER`
FROM
publications.titleauthor ta
LEFT JOIN publications.authors a
ON  ta.au_id = a.au_id
LEFT JOIN publications.titles t
ON ta.title_id = t.title_id
INNER JOIN publications.publishers p
ON t.pub_id = p.pub_id
ORDER BY a.au_id ASC;

-- Challenge 2
SELECT 
a.au_id 			as `AUTHOR ID`,
a.au_lname 			as `LAST NAME`,
a.au_fname 			as `FIRST NAME`,
p.pub_name 			as `PUBLISHER`,
COUNT(ta.title_id)	as `TITLE COUNT`
FROM
publications.titleauthor ta
LEFT JOIN publications.authors a
ON  ta.au_id = a.au_id
LEFT JOIN publications.titles t
ON ta.title_id = t.title_id
INNER JOIN publications.publishers p
ON t.pub_id = p.pub_id
GROUP BY a.au_id
ORDER BY a.au_id DESC;

-- Challenge 3
SELECT 
ta.au_id 			AS `AUTHOR ID`,
a.au_lname 			as `LAST NAME`,
a.au_fname 			as `FIRST NAME`,
SUM(t.ytd_sales) 	as TOTAL
FROM publications.titleauthor ta
INNER JOIN publications.titles t
ON ta.title_id = t.title_id
RIGHT JOIN publications.authors a
ON ta.au_id = a.au_id
GROUP BY ta.au_id
ORDER BY TOTAL DESC
LIMIT 3;

-- Challenge 4
