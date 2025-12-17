PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS FINES;
DROP TABLE IF EXISTS RESERVATIONS;
DROP TABLE IF EXISTS BORROW_TRANSACTIONS;
DROP TABLE IF EXISTS BOOKS;
DROP TABLE IF EXISTS STUDENTS;
DROP TABLE IF EXISTS LIBRARIANS;

-- LIBRARIANS
CREATE TABLE LIBRARIANS (
    librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- STUDENTS
CREATE TABLE STUDENTS (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    registration_date TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- BOOKS
CREATE TABLE BOOKS (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT UNIQUE,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publisher TEXT,
    publication_year INTEGER,
    category TEXT,
    location TEXT,
    quantity INTEGER DEFAULT 1,
    status TEXT DEFAULT 'Available' CHECK(status IN ('Available','Borrowed','Reserved','Maintenance')),
    date_added TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- BORROW TRANSACTIONS
CREATE TABLE BORROW_TRANSACTIONS (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    librarian_id INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active','Returned','Overdue')),
    is_overdue INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES STUDENTS(student_id) ON DELETE CASCADE,
    FOREIGN KEY (librarian_id) REFERENCES LIBRARIANS(librarian_id) ON DELETE CASCADE
);

-- RESERVATIONS
CREATE TABLE RESERVATIONS (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    reservation_date TEXT NOT NULL,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active','Fulfilled','Cancelled')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES STUDENTS(student_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- FINES
CREATE TABLE FINES (
    fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    fine_amount REAL NOT NULL,
    calculated_date TEXT NOT NULL,
    paid_date TEXT,
    payment_status TEXT DEFAULT 'Unpaid' CHECK(payment_status IN ('Unpaid','Paid','Waived')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES BORROW_TRANSACTIONS(transaction_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_book_status ON BOOKS(status);
CREATE INDEX idx_book_isbn ON BOOKS(isbn);
CREATE INDEX idx_student_email ON STUDENTS(email);
CREATE INDEX idx_transaction_status ON BORROW_TRANSACTIONS(status);
CREATE INDEX idx_transaction_dates ON BORROW_TRANSACTIONS(borrow_date, due_date);
CREATE INDEX idx_reservation_status ON RESERVATIONS(status);
CREATE INDEX idx_fine_payment_status ON FINES(payment_status);