few_shots = [
    {
        'Question': "How many Samsung phones do we have in stock?",
        'SQLQuery': "SELECT SUM(stock_quantity) FROM products WHERE brand = 'Samsung' AND category = 'Phone'",
        'SQLResult': "Result of the SQL query",
        'Answer': "125"
    },
    {
        'Question': "What is the total price of all laptops in inventory?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM products WHERE category = 'Laptop'",
        'SQLResult': "Result of the SQL query",
        'Answer': "285890"
    },
    {
        'Question': "If we sell all Apple products today with discounts applied, how much revenue will our store generate?",
        'SQLQuery': """SELECT SUM(a.total_amount * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) as total_revenue 
FROM (SELECT SUM(price * stock_quantity) as total_amount, product_id 
      FROM products WHERE brand = 'Apple' 
      GROUP BY product_id) a 
LEFT JOIN discounts ON a.product_id = discounts.product_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "267038.25"
    },
    {
        'Question': "How many headphones are available across all brands?",
        'SQLQuery': "SELECT SUM(stock_quantity) FROM products WHERE category = 'Headphones'",
        'SQLResult': "Result of the SQL query",
        'Answer': "510"
    },
    {
        'Question': "What is the total inventory value of all products?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM products",
        'SQLResult': "Result of the SQL query",
        'Answer': "1847541"
    },
    {
        'Question': "Which products have discounts greater than 10%?",
        'SQLQuery': """SELECT p.brand, p.category, p.model_name, d.pct_discount 
FROM products p 
JOIN discounts d ON p.product_id = d.product_id 
WHERE d.pct_discount > 10 
ORDER BY d.pct_discount DESC""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Dell Inspiron 15, Lenovo IdeaPad 3, Samsung Galaxy Tab A8, Garmin Forerunner 265, HP Pavilion 15, JBL Live Pro 2"
    },
    {
        'Question': "How much revenue will we generate if we sell all Dell laptops without discounts?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM products WHERE brand = 'Dell' AND category = 'Laptop'",
        'SQLResult': "Result of the SQL query",
        'Answer': "70470"
    },
    {
        'Question': "What is the average price of all smartwatches?",
        'SQLQuery': "SELECT AVG(price) FROM products WHERE category = 'Smartwatch'",
        'SQLResult': "Result of the SQL query",
        'Answer': "417"
    },
    {
        'Question': "How many products does Apple have across all categories?",
        'SQLQuery': "SELECT COUNT(*) FROM products WHERE brand = 'Apple'",
        'SQLResult': "Result of the SQL query",
        'Answer': "8"
    },
    {
        'Question': "If we sell all discounted products today, how much total revenue will we generate after applying discounts?",
        'SQLQuery': """SELECT SUM(p.price * p.stock_quantity * ((100 - d.pct_discount) / 100)) as discounted_revenue 
FROM products p 
JOIN discounts d ON p.product_id = d.product_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "179847.50"
    }
]
