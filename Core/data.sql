-- ==========================================
-- SAMPLE DATA INSERTION (from your provided samples)
-- ==========================================

-- LIBRARIANS
INSERT INTO LIBRARIANS (first_name, last_name, email, username, password, hire_date) VALUES
('John', 'Smith', 'john.smith@library.com', 'jsmith', 'hashed_password_1', '2020-01-15'),
('Maria', 'Garcia', 'maria.garcia@library.com', 'mgarcia', 'hashed_password_2', '2021-03-20'),
('David', 'Lopez', 'david.lopez@library.com', 'dlopez', 'hashed_password_3', '2022-05-10'),
('Sophia', 'Martinez', 'sophia.m@library.com', 'smartinez', 'hashed_password_4', '2023-01-12'),
('Ethan', 'Reyes', 'ethan.reyes@library.com', 'ereyes', 'hashed_password_5', '2023-09-20');

-- STUDENTS
INSERT INTO STUDENTS (first_name, last_name, email, phone, registration_date) VALUES
('Alice', 'Johnson', 'alice.j@email.com', '555-0101', '2024-09-01'),
('Bob', 'Williams', 'bob.w@email.com', '555-0102', '2024-09-01'),
('Carol', 'Brown', 'carol.b@email.com', '555-0103', '2024-09-15'),
('Daniel', 'Cruz', 'daniel.cruz@email.com', '555-0201', '2024-10-05'),
('Ella', 'Santos', 'ella.s@domain.com', '555-0202', '2024-10-05'),
('Frank', 'Gomez', 'frank.g@domain.com', '555-0203', '2024-10-10'),
('Grace', 'Rivera', 'grace.r@domain.com', '555-0204', '2024-10-15'),
('Henry', 'Torres', 'henry.t@domain.com', '555-0205', '2024-10-20');

-- BOOKS
INSERT INTO BOOKS (isbn, title, author, publisher, publication_year, category, location, quantity, status, date_added) VALUES
('978-0-7475-3269-9', 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Bloomsbury', 1997, 'Fiction', 'A-101', 7, 'Available', '2024-01-10'),
('978-0-452-28423-4', '1984', 'George Orwell', 'Penguin Books', 1949, 'Fiction', 'A-205', 3, 'Available', '2024-01-10'),
('978-0-06-112008-4', 'To Kill a Mockingbird', 'Harper Lee', 'HarperCollins', 1960, 'Fiction', 'A-150', 9, 'Borrowed', '2024-01-10'),
('978-0-13-468599-1', 'Database System Concepts', 'Abraham Silberschatz', 'McGraw-Hill', 2019, 'Computer Science', 'B-301', 5, 'Available', '2024-01-15'),
('978-1-4028-9462-6', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925, 'Fiction', 'A-110', 2, 'Available', '2024-01-20'),
('978-0-7432-7356-5', 'Angels & Demons', 'Dan Brown', 'Pocket Books', 2000, 'Thriller', 'A-220', 6, 'Available', '2024-01-21'),
('978-0-316-76948-8', 'The Silent Patient', 'Alex Michaelides', 'Celadon Books', 2019, 'Mystery', 'A-230', 8, 'Borrowed', '2024-01-25'),
('978-0-321-63536-9', 'Introduction to Algorithms', 'Cormen, Leiserson, Rivest, Stein', 'MIT Press', 2009, 'Computer Science', 'B-310', 4, 'Available', '2024-02-01'),
('978-1-119-97206-3', 'Python Crash Course', 'Eric Matthes', 'No Starch Press', 2015, 'Computer Science', 'B-320', 10, 'Reserved', '2024-02-05'),
('978-0-452-28425-8', 'Animal Farm', 'George Orwell', 'Penguin Books', 1945, 'Fiction', 'A-206', 1, 'Available', '2024-02-08');

-- BORROW TRANSACTIONS
INSERT INTO BORROW_TRANSACTIONS (book_id, student_id, librarian_id, borrow_date, due_date, return_date, status, is_overdue) VALUES
(3, 1, 1, '2024-11-01', '2024-11-15', NULL, 'Active', 0),
(7, 2, 3, '2024-11-02', '2024-11-16', NULL, 'Active', 0),
(1, 4, 1, '2024-11-05', '2024-11-19', '2024-11-18', 'Returned', 0),
(2, 3, 2, '2024-11-07', '2024-11-21', NULL, 'Overdue', 1),
(10, 5, 4, '2024-11-10', '2024-11-24', NULL, 'Active', 0),
(8, 6, 5, '2024-11-11', '2024-11-25', NULL, 'Active', 0);

-- RESERVATIONS
INSERT INTO RESERVATIONS (book_id, student_id, reservation_date, status, expires_at) VALUES
(4, 1, '2025-01-12', 'Active', '2025-01-17 23:59:59'),
(5, 2, '2025-01-13', 'Active', '2025-01-18 23:59:59'),
(6, 3, '2025-01-14', 'Cancelled', NULL),
(7, 4, '2025-01-15', 'Fulfilled', NULL),
(8, 5, '2025-01-16', 'Active', '2025-01-21 23:59:59'),
(9, 6, '2025-01-17', 'Active', '2025-01-22 23:59:59'),
(10, 7, '2025-01-18', 'Cancelled', NULL),
(2, 8, '2025-01-19', 'Active', '2025-01-24 23:59:59');

-- FINES
INSERT INTO FINES (transaction_id, fine_amount, calculated_date, paid_date, payment_status) VALUES
(2, 50.00, '2024-11-22', '2024-11-24', 'Paid'),
(3, 75.00, '2024-11-23', NULL, 'Unpaid'),
(3, 25.00, '2024-11-24', NULL, 'Unpaid'),
(1, 15.00, '2024-11-20', '2024-11-21', 'Paid'),
(4, 30.00, '2024-11-26', NULL, 'Unpaid');