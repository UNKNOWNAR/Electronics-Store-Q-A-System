-- Create the database
CREATE DATABASE electronics_store;

-- Connect to the database
\c electronics_store;

-- Create the products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    specs VARCHAR(200),
    price INT CHECK (price BETWEEN 100 AND 5000),
    stock_quantity INT NOT NULL,
    UNIQUE (brand, category, model_name)
);

-- Create the discounts table
CREATE TABLE discounts (
    discount_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert sample data for products
INSERT INTO products (brand, category, model_name, specs, price, stock_quantity) VALUES
-- Laptops
('Apple', 'Laptop', 'MacBook Air M2', '256GB SSD, 8GB RAM', 1199, 25),
('Apple', 'Laptop', 'MacBook Pro 14"', '512GB SSD, 16GB RAM', 1999, 15),
('Dell', 'Laptop', 'XPS 13', '512GB SSD, 16GB RAM', 1299, 30),
('Dell', 'Laptop', 'Inspiron 15', '256GB SSD, 8GB RAM', 699, 45),
('HP', 'Laptop', 'Pavilion 15', '512GB SSD, 8GB RAM', 799, 40),
('HP', 'Laptop', 'Envy x360', '1TB SSD, 16GB RAM', 1199, 20),
('Lenovo', 'Laptop', 'ThinkPad X1', '512GB SSD, 16GB RAM', 1499, 18),
('Lenovo', 'Laptop', 'IdeaPad 3', '256GB SSD, 8GB RAM', 599, 50),

-- Phones
('Apple', 'Phone', 'iPhone 15', '128GB', 799, 60),
('Apple', 'Phone', 'iPhone 15 Pro', '256GB', 999, 40),
('Samsung', 'Phone', 'Galaxy S24', '256GB', 899, 55),
('Samsung', 'Phone', 'Galaxy A54', '128GB', 449, 70),
('Google', 'Phone', 'Pixel 8', '128GB', 699, 35),
('Google', 'Phone', 'Pixel 8 Pro', '256GB', 999, 25),
('OnePlus', 'Phone', 'OnePlus 12', '256GB', 799, 30),
('Xiaomi', 'Phone', 'Xiaomi 13', '256GB', 649, 40),

-- Tablets
('Apple', 'Tablet', 'iPad Air', '64GB', 599, 45),
('Apple', 'Tablet', 'iPad Pro 11"', '128GB', 799, 30),
('Samsung', 'Tablet', 'Galaxy Tab S9', '128GB', 699, 35),
('Samsung', 'Tablet', 'Galaxy Tab A8', '64GB', 299, 50),
('Lenovo', 'Tablet', 'Tab P11', '128GB', 349, 40),
('Microsoft', 'Tablet', 'Surface Go 3', '128GB', 549, 25),

-- Headphones
('Apple', 'Headphones', 'AirPods Pro 2', 'Active Noise Cancellation', 249, 100),
('Sony', 'Headphones', 'WH-1000XM5', 'Over-ear, ANC', 399, 60),
('Sony', 'Headphones', 'WF-1000XM5', 'In-ear, ANC', 299, 75),
('Bose', 'Headphones', 'QuietComfort Ultra', 'Over-ear, ANC', 429, 45),
('Samsung', 'Headphones', 'Galaxy Buds2 Pro', 'In-ear, ANC', 229, 85),
('JBL', 'Headphones', 'Live Pro 2', 'In-ear, ANC', 149, 90),
('Beats', 'Headphones', 'Studio Pro', 'Over-ear, ANC', 349, 55),

-- Smartwatches
('Apple', 'Smartwatch', 'Apple Watch Series 9', 'GPS, 41mm', 399, 70),
('Apple', 'Smartwatch', 'Apple Watch Ultra 2', 'GPS, 49mm', 799, 30),
('Samsung', 'Smartwatch', 'Galaxy Watch 6', 'GPS, 40mm', 299, 60),
('Samsung', 'Smartwatch', 'Galaxy Watch 6 Classic', 'GPS, 43mm', 399, 45),
('Fitbit', 'Smartwatch', 'Sense 2', 'Health & Fitness', 299, 50),
('Garmin', 'Smartwatch', 'Forerunner 265', 'Running GPS', 449, 35),

-- Monitors
('Dell', 'Monitor', 'UltraSharp U2723DE', '27" 4K USB-C', 699, 25),
('LG', 'Monitor', 'UltraGear 27GN950', '27" 4K Gaming 144Hz', 799, 20),
('Samsung', 'Monitor', 'Odyssey G7', '32" 4K Gaming', 899, 18),
('ASUS', 'Monitor', 'ProArt PA279CV', '27" 4K Professional', 549, 22),
('BenQ', 'Monitor', 'PD2725U', '27" 4K Designer', 749, 15);

-- Insert discounts
INSERT INTO discounts (product_id, pct_discount) VALUES
(1, 10.00),   -- MacBook Air M2
(4, 15.00),   -- Dell Inspiron 15
(5, 12.00),   -- HP Pavilion 15
(8, 20.00),   -- Lenovo IdeaPad 3
(9, 5.00),    -- iPhone 15
(12, 10.00),  -- Samsung Galaxy A54
(14, 8.00),   -- Google Pixel 8 Pro
(22, 15.00),  -- Samsung Galaxy Tab A8
(26, 12.00),  -- JBL Live Pro 2
(30, 10.00),  -- Samsung Galaxy Watch 6 Classic
(32, 15.00),  -- Garmin Forerunner 265
(35, 10.00),  -- Samsung Odyssey G7
(37, 8.00);   -- BenQ PD2725U

-- Verify data
SELECT 'Products Count:' as info, COUNT(*) as count FROM products
UNION ALL
SELECT 'Discounts Count:' as info, COUNT(*) as count FROM discounts;

-- Sample query: Products with discounts
SELECT 
    p.brand,
    p.category,
    p.model_name,
    p.price,
    p.stock_quantity,
    d.pct_discount,
    ROUND(p.price * (100 - COALESCE(d.pct_discount, 0)) / 100) as discounted_price
FROM products p
LEFT JOIN discounts d ON p.product_id = d.product_id
WHERE d.pct_discount IS NOT NULL
ORDER BY p.category, p.brand;
