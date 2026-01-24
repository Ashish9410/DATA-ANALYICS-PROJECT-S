use  customer_behavior;

SELECT *
FROM customer_shopping_cleaned;

SELECT `Gender`,SUM(`Purchase Amount (USD)`) AS revenue
FROM customer_shopping_cleaned
GROUP BY `Gender`;

SELECT `Customer ID`, `Purchase Amount (USD)`
FROM customer_shopping_cleaned
WHERE `Discount Applied` = 'Yes'AND `Purchase Amount (USD)` >(SELECT AVG(`Purchase Amount (USD)`)
FROM customer_shopping_cleaned);


SELECT `Shipping Type`,ROUND(AVG(`Purchase Amount (USD)`), 2) AS avg_purchase
FROM customer_shopping_cleaned
WHERE `Shipping Type` IN ('Standard', 'Express')
GROUP BY `Shipping Type`;

SELECT `Subscription Status`,
       COUNT(`Customer ID`) AS total_customers,
       ROUND(AVG(`Purchase Amount (USD)`), 2) AS avg_spend,
       ROUND(SUM(`Purchase Amount (USD)`), 2) AS total_revenue
FROM customer_shopping_cleaned
GROUP BY `Subscription Status`
ORDER BY total_revenue DESC;

SELECT `Item Purchased`,ROUND(100.0 * SUM(CASE WHEN `Discount Applied` = 'Yes' THEN 1 ELSE 0 END)/ COUNT(*),2) AS discount_percentage
FROM customer_shopping_cleaned
GROUP BY `Item Purchased`
ORDER BY discount_percentage DESC
LIMIT 5;

WITH customer_segment AS (
    SELECT `Customer ID`,
           CASE
               WHEN `Previous Purchases` = 1 THEN 'New'
               WHEN `Previous Purchases` BETWEEN 2 AND 10 THEN 'Returning'
               ELSE 'Loyal'
           END AS segment
    FROM customer_shopping_cleaned
)
SELECT segment,COUNT(*) AS number_of_customers
FROM customer_segment
GROUP BY segment;


WITH product_rank AS (SELECT `Category`,`Item Purchased`,COUNT(*) AS total_orders,
ROW_NUMBER() OVER (PARTITION BY `Category`ORDER BY COUNT(*) DESC) AS rnk
FROM customer_shopping_cleaned
GROUP BY `Category`, `Item Purchased`
)
SELECT `Category`, `Item Purchased`, total_orders
FROM product_rank
WHERE rnk <= 3;


SELECT `Subscription Status`,COUNT(`Customer ID`) AS repeat_buyers
FROM customer_shopping_cleaned
WHERE `Previous Purchases` > 5
GROUP BY `Subscription Status`;



SELECT CASE
	WHEN Age < 25 THEN 'Under 25'
	WHEN Age BETWEEN 25 AND 40 THEN '25–40'
	WHEN Age BETWEEN 41 AND 60 THEN '41–60'
	ELSE '60+'
END AS age_group,
SUM(`Purchase Amount (USD)`) AS total_revenue
FROM customer_shopping_cleaned
GROUP BY age_group
ORDER BY total_revenue DESC;

