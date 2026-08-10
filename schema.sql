-- Reset table
DROP TABLE IF EXISTS books;

-- Create table schema
CREATE TABLE books (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  cover_url TEXT NOT NULL,
  b2_key TEXT NOT NULL
);

-- Seed book catalog
INSERT INTO books (id, title, author, cover_url, b2_key) VALUES
('clean_code', 'Clean Code', 'Robert C. Martin', 'https://via.placeholder.com/150', 'clean_code'),
('pragmatic_programmer', 'The Pragmatic Programmer', 'Andrew Hunt', 'https://via.placeholder.com/150', 'pragmatic_programmer');