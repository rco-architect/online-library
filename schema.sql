-- Reset tables
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;

-- 1. Create Categories Table
CREATE TABLE categories (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

-- 2. Create Books Table with Category Reference
CREATE TABLE books (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  cover_url TEXT NOT NULL,
  b2_key TEXT NOT NULL,
  category_id TEXT NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Seed Categories
INSERT INTO categories (id, name) VALUES
('software_engineering', 'Software Engineering'),
('computer_science', 'Computer Science'),
('artificial_intelligence', 'Artificial Intelligence',algorithms'),
('data_science', 'Data Science'),
('web_development', 'Web Development');

-- Seed Books
INSERT INTO books (id, title, author, cover_url, b2_key, category_id) VALUES
('clean_code', 'Clean Code', 'Robert C. Martin', 'https://via.placeholder.com/150', 'clean_code', 'software_engineering'),
('pragmatic_programmer', 'The Pragmatic Programmer', 'Andrew Hunt', 'https://via.placeholder.com/150', 'pragmatic_programmer', 'software_engineering');