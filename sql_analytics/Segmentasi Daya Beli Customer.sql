SELECT 
    CASE 
        WHEN annual_income < 45000 THEN 'Budget Customer'
        WHEN annual_income BETWEEN 45000 AND 85000 THEN 'Middle Class'
        ELSE 'High Net Worth' 
    END AS income_class,
    COUNT(car_id) as total_buyers,
    AVG(profit) as avg_profit_generated
FROM car_sales_data
GROUP BY 1
ORDER BY avg_profit_generated DESC;