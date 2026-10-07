-- Create prices table
CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price_value DECIMAL(10, 2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_prices_product_name ON prices(product_name);
CREATE INDEX IF NOT EXISTS idx_prices_created_at ON prices(created_at);

-- Insert sample data (optional)
INSERT INTO prices (product_name, price_value, description) VALUES
    ('Product A', 99.99, 'First product'),
    ('Product B', 149.50, 'Second product'),
    ('Product C', 79.99, 'Third product')
ON CONFLICT DO NOTHING;
