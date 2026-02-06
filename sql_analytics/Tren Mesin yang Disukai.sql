SELECT 
    engine_type,
    COUNT(*) as units_sold,
    SUM(profit) as total_profit
FROM car_sales_data
GROUP BY engine_type;