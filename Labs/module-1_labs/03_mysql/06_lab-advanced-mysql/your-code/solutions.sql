-- Labs/module-1_labs/03_mysql/06_lab-advanced-mysql/

USE publications;

-- step 1
WITH royalties AS (
	SELECT 
		t.title_id 						AS title_id,
		ta.au_id 						AS au_id,
		(t.price * s.qty * t.royalty / 100 * ta.royaltyper / 100) AS royalty
	FROM titles t
	LEFT JOIN titleauthor ta 
		ON t.title_id = ta.title_id
	LEFT JOIN sales s 
		ON t.title_id = s.title_id),
    
-- step 2
au_title_royalty AS (
	SELECT
		title_id,
		au_id,
		SUM(royalty) AS au_tit_roy
	FROM royalties
    GROUP BY au_id, title_id)
    
-- step 3
/*
SELECT 
	ta.au_id AS 'Author ID',
    SUM((t.advance * ta.royaltyper / 100) + atr.au_tit_roy) AS Profits
FROM titleauthor ta
INNER JOIN au_title_royalty atr
	ON ta.au_id = atr.au_id
INNER JOIN titles t 
	ON ta.title_id = t.title_id
GROUP BY ta.au_id
ORDER BY Profits DESC
LIMIT 3;

-- Challenge 2
SELECT 
	ta.au_id AS 'Author ID',
    SUM((t.advance * ta.royaltyper / 100) + atr.au_tit_roy) AS Profits
FROM titleauthor ta
INNER JOIN (
		SELECT
			title_id,
			au_id,
			SUM(royalty) AS au_tit_roy
		FROM (
			SELECT 
				t.title_id 						AS title_id,
				ta.au_id 						AS au_id,
				(t.price * s.qty * t.royalty / 100 * ta.royaltyper / 100) AS royalty
			FROM titles t
			LEFT JOIN titleauthor ta 
				ON t.title_id = ta.title_id
			LEFT JOIN sales s 
				ON t.title_id = s.title_id
			) royalties
		GROUP BY au_id, title_id
		) atr
	ON ta.au_id = atr.au_id
INNER JOIN titles t 
	ON ta.title_id = t.title_id
GROUP BY ta.au_id
ORDER BY Profits DESC
LIMIT 3;
*/
-- Challenge 3

-- to execute comment out step 3 and challenge 2

CREATE TEMPORARY TABLE most_profiting_authors AS
SELECT 
	ta.au_id AS 'Author ID',
    SUM((t.advance * ta.royaltyper / 100) + atr.au_tit_roy) AS Profits
FROM titleauthor ta
INNER JOIN au_title_royalty atr
	ON ta.au_id = atr.au_id
INNER JOIN titles t 
	ON ta.title_id = t.title_id
GROUP BY ta.au_id
ORDER BY Profits DESC;


/*
Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds 
to your MySQL server version for the right syntax to use near 'CREATE TEMPORARY TABLE 
most_profiting_authors AS SELECT   ta.au_id AS 'Author ID' at line 69

	
	
*/