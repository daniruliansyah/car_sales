WITH DealerRank AS (
    SELECT 
        dealer_region,
        dealer_name,
        SUM(profit) as total_profit,
        DENSE_RANK() OVER (PARTITION BY dealer_region ORDER BY SUM(profit) DESC) as rank_in_region
    FROM car_sales_data
    GROUP BY dealer_region, dealer_name
)
SELECT * FROM DealerRank
WHERE rank_in_region <= 3;