-- ================================
-- Database Schema for Leave Management System
-- ================================

-- Employees table
CREATE TABLE employees (
    id INT PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    department VARCHAR(100),
    joining_date DATE,
    total_leaves INT DEFAULT 20,
    used_leaves INT DEFAULT 0
);

-- Leaves table
CREATE TABLE leaves (
    id INT PRIMARY KEY AUTOINCREMENT,
    employee_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    approved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
);

-- Leave Transactions table
CREATE TABLE leave_transactions (
    id INT PRIMARY KEY AUTOINCREMENT,
    leave_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,  -- e.g., CREATED, APPROVED, REJECTED
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (leave_id) REFERENCES leaves(id) ON DELETE CASCADE
);

-- Indexes for faster queries
CREATE INDEX idx_employee_email ON employees(email);
CREATE INDEX idx_leave_employee ON leaves(employee_id);
CREATE INDEX idx_transaction_leave ON leave_transactions(leave_id);
