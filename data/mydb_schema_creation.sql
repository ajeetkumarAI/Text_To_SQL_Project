-- Create the database for mY Industries
CREATE DATABASE IF NOT EXISTS mydb;

USE mydb;

-- Table: Customers
CREATE TABLE customers (
  customer_id VARCHAR(10) PRIMARY KEY,
  company_name VARCHAR(100),
  contact_name VARCHAR(100),
  city VARCHAR(50),
  country VARCHAR(50)
);

-- Table: Orders
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id VARCHAR(10),
  order_date DATE,
  ship_city VARCHAR(50),
  freight FLOAT,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Table: Order Details
CREATE TABLE order_details (
  order_id INT,
  product_id INT,
  quantity INT,
  unit_price FLOAT,
  PRIMARY KEY (order_id, product_id)
);

-- Table: Products
CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(100),
  supplier_id INT,
  category VARCHAR(50),
  unit_price FLOAT
);

-- Table: Suppliers
CREATE TABLE suppliers (
  supplier_id INT PRIMARY KEY,
  company_name VARCHAR(100),
  contact_name VARCHAR(100),
  city VARCHAR(50),
  country VARCHAR(50)
);


