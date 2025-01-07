CREATE TABLE ads (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(50) NOT NULL, -- e.g., Amazon, Alibaba
    product_id VARCHAR(100) NOT NULL UNIQUE, -- Unique product identifier from the source
    title TEXT NOT NULL, -- Product title
    description TEXT, -- Detailed description
    category VARCHAR(100) NOT NULL, -- Product category
    brand VARCHAR(100), -- Brand name (nullable)
    price_original DECIMAL(10, 2) NOT NULL, -- Original price of the product
    price_discounted DECIMAL(10, 2), -- Discounted price (nullable)
    currency VARCHAR(10) NOT NULL, -- Currency code (e.g., USD)
    affiliate_link TEXT NOT NULL, -- Affiliate tracking link
    image_urls JSON NOT NULL, -- JSON array of image URLs
    rating FLOAT, -- Average rating (nullable)
    review_count INT, -- Number of reviews (nullable)
    stock_status BOOLEAN NOT NULL DEFAULT TRUE, -- Availability status
    shipping_cost DECIMAL(10, 2), -- Shipping cost (nullable)
    delivery_time VARCHAR(100), -- Estimated delivery time (nullable)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Last update timestamp
);

INSERT INTO ads (
    source, product_id, title, description, category, brand, price_original,
    price_discounted, currency, affiliate_link, image_urls, rating, review_count,
    stock_status, shipping_cost, delivery_time, created_at, updated_at
) VALUES (
    'Amazon', 'B07FZ8S74R', 'Product Name', 'Detailed description here', 'Electronics',
    'Brand Name', 100.00, 80.00, 'USD', 'https://affiliate-link',
    '["https://image1.jpg", "https://image2.jpg"]', 4.5, 200, true,
    10.00, '5-10 days', NOW(), NOW()
);
