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
        'Answer': "243257"
    },
    {
        'Question': "If we sell all Apple products today with discounts applied, how much revenue will our store generate?",
        'SQLQuery': """SELECT SUM(a.total_amount * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) as total_revenue 
FROM (SELECT SUM(price * stock_quantity) as total_amount, product_id 
      FROM products WHERE brand = 'Apple' 
      GROUP BY product_id) a 
LEFT JOIN discounts ON a.product_id = discounts.product_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "267397.50"
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
        'Answer': "963477"
    },
    {
        'Question': "Which products have discounts greater than 10%?",
        'SQLQuery': """SELECT p.brand, p.category, p.model_name, d.pct_discount 
FROM products p 
JOIN discounts d ON p.product_id = d.product_id 
WHERE d.pct_discount > 10 
ORDER BY d.pct_discount DESC""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Lenovo IdeaPad 3, Dell Inspiron 15, Microsoft Surface Go 3, Samsung Galaxy Watch 6, HP Pavilion 15, Bose QuietComfort Ultra"
    },
    {
        'Question': "How much revenue will we generate if we sell all Dell laptops without discounts?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM products WHERE brand = 'Dell' AND category = 'Laptop'",
        'SQLResult': "Result of the SQL query",
        'Answer': "70425"
    },
    {
        'Question': "What is the average price of all smartwatches?",
        'SQLQuery': "SELECT AVG(price) FROM products WHERE category = 'Smartwatch'",
        'SQLResult': "Result of the SQL query",
        'Answer': "440.67"
    },
    {
        'Question': "How many products does Apple have across all categories?",
        'SQLQuery': "SELECT COUNT(*) FROM products WHERE brand = 'Apple'",
        'SQLResult': "Result of the SQL query",
        'Answer': "9"
    },
    {
        'Question': "If we sell all discounted products today, how much total revenue will we generate after applying discounts?",
        'SQLQuery': """SELECT SUM(p.price * p.stock_quantity * ((100 - d.pct_discount) / 100)) as discounted_revenue 
FROM products p 
JOIN discounts d ON p.product_id = d.product_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "300491.80"
    },
    {
        'Question': "What are the top 5 most expensive products in the store?",
        'SQLQuery': "SELECT model_name, price FROM products ORDER BY price DESC LIMIT 5",
        'SQLResult': "Result of the SQL query",
        'Answer': "MacBook Pro 16, Dell XPS 17, Surface Book 3, etc."
    },
    {
        'Question': "What is the average discount percentage for products with a discount?",
        'SQLQuery': "SELECT AVG(pct_discount) FROM discounts",
        'SQLResult': "Result of the SQL query",
        'Answer': "12.5%"
    },
    {
        'Question': "How many products are there in each category?",
        'SQLQuery': "SELECT category, COUNT(*) FROM products GROUP BY category",
        'SQLResult': "Result of the SQL query",
        'Answer': "Laptops: 10, Phones: 8, etc."
    },
    {
        'Question': "Which products have a stock quantity of less than 20?",
        'SQLQuery': "SELECT model_name, stock_quantity FROM products WHERE stock_quantity < 20",
        'SQLResult': "Result of the SQL query",
        'Answer': "MacBook Pro 16, Surface Go 3, etc."
    },
    {
        'Question': "What is the total number of products from the 'Dell' brand?",
        'SQLQuery': "SELECT COUNT(*) FROM products WHERE brand = 'Dell'",
        'SQLResult': "Result of the SQL query",
        'Answer': "5"
    },
    {
        'Question': "What is the most expensive phone in the store?",
        'SQLQuery': "SELECT model_name, price FROM products WHERE category = 'Phone' ORDER BY price DESC LIMIT 1",
        'SQLResult': "Result of the SQL query",
        'Answer': "iPhone 15 Pro Max"
    },
    {
        'Question': "What is the total stock of all products from the 'HP' brand?",
        'SQLQuery': "SELECT SUM(stock_quantity) FROM products WHERE brand = 'HP'",
        'SQLResult': "Result of the SQL query",
        'Answer': "150"
    },
    {
        'Question': "Which products have no discount?",
        'SQLQuery': "SELECT model_name FROM products WHERE product_id NOT IN (SELECT product_id FROM discounts)",
        'SQLResult': "Result of the SQL query",
        'Answer': "iPhone 15, Google Pixel 8, etc."
    },
    {
        'Question': "What is the average price of products for each brand?",
        'SQLQuery': "SELECT brand, AVG(price) FROM products GROUP BY brand",
        'SQLResult': "Result of the SQL query",
        'Answer': "Apple: $1500, Samsung: $800, etc."
    },
    {
        'Question': "How many products have a price between $500 and $1000?",
        'SQLQuery': "SELECT COUNT(*) FROM products WHERE price BETWEEN 500 AND 1000",
        'SQLResult': "Result of the SQL query",
        'Answer': "12"
    },
    {
        'Question': "What are the names and specs of all 'Lenovo' laptops?",
        'SQLQuery': "SELECT model_name, specs FROM products WHERE brand = 'Lenovo' AND category = 'Laptop'",
        'SQLResult': "Result of the SQL query",
        'Answer': "ThinkPad X1 Carbon: 16GB RAM, 512GB SSD, etc."
    },
    {
        'Question': "What is the total value of all 'Samsung' products in stock?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM products WHERE brand = 'Samsung'",
        'SQLResult': "Result of the SQL query",
        'Answer': "150000"
    },
    {
        'Question': "Which category has the highest number of products?",
        'SQLQuery': "SELECT category, COUNT(*) as product_count FROM products GROUP BY category ORDER BY product_count DESC LIMIT 1",
        'SQLResult': "Result of the SQL query",
        'Answer': "Laptop"
    },
    {
        'Question': "What is the minimum price of a product in the 'Headphones' category?",
        'SQLQuery': "SELECT MIN(price) FROM products WHERE category = 'Headphones'",
        'SQLResult': "Result of the SQL query",
        'Answer': "50"
    },
    {
        'Question': "List all products with their discount percentage, if they have one.",
        'SQLQuery': "SELECT p.model_name, d.pct_discount FROM products p LEFT JOIN discounts d ON p.product_id = d.product_id",
        'SQLResult': "Result of the SQL query",
        'Answer': "MacBook Air M2: 10%, etc."
    },
    {
        'Question': "What is the total number of discounted products?",
        'SQLQuery': "SELECT COUNT(*) FROM discounts",
        'SQLResult': "Result of the SQL query",
        'Answer': "8"
    },
    {
        'Question': "Which brand has the most products in stock?",
        'SQLQuery': "SELECT brand, SUM(stock_quantity) as total_stock FROM products GROUP BY brand ORDER BY total_stock DESC LIMIT 1",
        'SQLResult': "Result of the SQL query",
        'Answer': "Samsung"
    },
    {
        'Question': "What is the average price of laptops from 'Dell'?",
        'SQLQuery': "SELECT AVG(price) FROM products WHERE brand = 'Dell' AND category = 'Laptop'",
        'SQLResult': "Result of the SQL query",
        'Answer': "1100"
    },
    {
        'Question': "List all products sorted by brand and then by price.",
        'SQLQuery': "SELECT brand, model_name, price FROM products ORDER BY brand, price",
        'SQLResult': "Result of the SQL query",
        'Answer': "Apple, iPhone 15, $799, etc."
    },
    {
        'Question': "What is the total revenue we can get from products with a stock of more than 50?",
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM products WHERE stock_quantity > 50",
        'SQLResult': "Result of the SQL query",
        'Answer': "250000"
    }
]
