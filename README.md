

# Online Library Vault

A cloud-native, serverless digital library vault and PDF reader application built on Cloudflare's edge network, Backblaze B2 object storage, and a local Python Flask management dashboard.

  

## 🏗️ System Architecture & Workflow

Plaintext

```
[ Local PC / Flask Dashboard ] ──(D1 SQL Sync)──► [ Cloudflare D1 (Edge SQLite DB) ]
             │                                              │
             ▼ (Git Push)                                   ▼ (JSON Catalog & Categories)
     [ GitHub Repo ] ──(Deploy)──► [ Cloudflare Pages ] ◄───┤
                                    (Web Frontend)          │ (Presigned B2 PDF URLs)
                                                            ▼
                                                [ Cloudflare Worker Gateway ] ──► [ Backblaze B2 Storage ]
```

1. **Frontend (Cloudflare Pages):** Displays a responsive, dark-mode catalog with category filtering and renders PDFs using a custom web viewer.
    
      
    
2. **API Gateway (Cloudflare Worker):** Handles edge requests, queries the Cloudflare D1 database for dynamic catalog lists, and generates secure AWS SigV4 presigned URLs to access private PDF files stored in Backblaze B2.
    
      
    
3. **Database (Cloudflare D1):** Edge-hosted SQLite relational database storing categories, book metadata, cover image URLs, and storage keys.
    
      
    
4. **Storage (Backblaze B2):** Secure object storage bucket (`private-pdf-vault`) housing the raw PDF assets.
    
      
    
5. **Local Management (Python Flask):** A local dashboard (`app.py`) for visually managing books, auto-exporting `schema.sql`, and syncing changes to the remote Cloudflare D1 instance.
    
      
    

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3 (CSS Variables, Flexbox/Grid), Modern Vanilla JS (Async/Fetch API).
    
      
    
- **Serverless Backend:** Cloudflare Workers (JavaScript, AWS SigV4 Request Signing).
    
      
    
- **Database Engine:** Cloudflare D1 (Distributed SQLite at the edge).
    
      
    
- **Object Storage:** Backblaze B2 (S3-Compatible API).
    
      
    
- **Local Control Panel:** Python 3 (Flask, SQLite3).
    
      
    
- **Hosting & CI/CD:** Cloudflare Pages & GitHub.
    
      
    

## 📂 Project Directory Structure

Plaintext

```
online-library/
├── src/
│   ├── css/
│   │   └── styles.css        # Responsive dark-mode styling & filter bar components
│   ├── js/
│   │   └── app.js            # Dynamic API fetch logic & category filtering
│   └── pages/
│       └── reader.html       # Dynamic PDF viewer page consuming presigned URLs
├── .gitignore                # Excludes virtual environments, binaries, and local configs
├── app.py                    # Local Flask GUI management app for books/categories
├── index.html                # Main catalog landing page
├── Open_Dashboard.bat        # One-click Windows batch runner for local Flask app
├── schema.sql                # Complete database structure and seed data export
└── wrangler.json             # Cloudflare Pages build configuration
```

## 🗄️ Relational Database Schema (`schema.sql`)

SQL

```
-- Reset database structure
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;

-- 1. Categories Table
CREATE TABLE categories (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

-- 2. Books Table (Linked via Foreign Key)
CREATE TABLE books (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  cover_url TEXT NOT NULL,
  b2_key TEXT NOT NULL,
  category_id TEXT NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Default Category Seeds
INSERT INTO categories (id, name) VALUES
('software_engineering', 'Software Engineering'),
('computer_science', 'Computer Science'),
('artificial_intelligence', 'Artificial Intelligence'),
('data_science', 'Data Science'),
('algorithms', 'Algorithms'),
('web_development', 'Web Development');

-- Sample Book Records
INSERT INTO books (id, title, author, cover_url, b2_key, category_id) VALUES
('clean_code', 'Clean Code', 'Robert C. Martin', 'https://covers.openlibrary.org/b/isbn/0132350882-L.jpg', 'clean_code', 'software_engineering'),
('pragmatic_programmer', 'The Pragmatic Programmer', 'Andrew Hunt', 'https://covers.openlibrary.org/b/isbn/0135957052-L.jpg', 'pragmatic_programmer', 'software_engineering');
```

## ⚙️ Cloudflare Worker Gateway (`b2-pdf-gateway`)

The Worker exposes three key operational endpoints:

  

1. `GET /api/categories`: Queries D1 (`SELECT * FROM categories`) to generate category filter buttons dynamically.
    
      
    
2. `GET /api/books`: Executes a `LEFT JOIN` query between `books` and `categories` to supply full catalog metadata with human-readable category names.
    
      
    
3. `GET /?book={b2_key}`: Generates an AWS SigV4 signed URL allowing temporary (15-minute) authenticated access to private PDF objects stored in Backblaze B2.
    
      
    

## 🚀 Operations & Deployment Commands

### 1. Local Management Dashboard

Run the dashboard via terminal or double-click `Open_Dashboard.bat`:

  

PowerShell

```
.\.venv\Scripts\Activate.ps1
python app.py
```

_Access local control GUI at `[http://127.0.0.1:5000](http://127.0.0.1:5000)`._

### 2. Sync Local Database Changes to Remote Cloudflare D1

PowerShell

```
npx wrangler d1 execute my-library-db --remote --file=./schema.sql
```

### 3. Deploy Web Frontend to Cloudflare Pages

PowerShell

```
# Commit updates to version control
git add .
git commit -m "Update application features"
git push origin main

# Deploy to Cloudflare Pages
npx wrangler pages deploy . --project-name=rco-library
```