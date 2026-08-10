const BASE_WORKER_URL = 'https://b2-pdf-gateway.rco-architect.workers.dev';
let allBooks = [];

async function initLibrary() {
  const catalogElement = document.getElementById('catalog');

  try {
    // Fetch categories and books simultaneously
    const [catRes, bookRes] = await Promise.all([
      fetch(`${BASE_WORKER_URL}/api/categories`),
      fetch(`${BASE_WORKER_URL}/api/books`)
    ]);

    if (!catRes.ok || !bookRes.ok) {
      throw new Error('Failed to fetch library resources');
    }

    const categories = await catRes.json();
    allBooks = await bookRes.json();

    renderCategories(categories);
    renderBooks(allBooks);
  } catch (err) {
    console.error('Error loading library:', err);
    catalogElement.innerHTML = `
      <div class="status-msg" style="color: #f87171;">
        Failed to load library catalog.<br>
        <small style="color: #94a3b8;">Ensure Cloudflare D1 binding "DB" is attached to the Worker.</small>
      </div>
    `;
  }
}

function renderCategories(categories) {
  const filterBar = document.getElementById('filter-bar');
  categories.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'filter-btn';
    btn.textContent = cat.name;
    btn.onclick = () => filterCategory(cat.id, btn);
    filterBar.appendChild(btn);
  });
}

function renderBooks(books) {
  const catalog = document.getElementById('catalog');
  catalog.innerHTML = '';

  if (books.length === 0) {
    catalog.innerHTML = '<div class="status-msg">No books found in this category.</div>';
    return;
  }

  books.forEach(book => {
    const card = document.createElement('div');
    card.className = 'book-card';
    card.onclick = () => {
      window.location.href = `src/pages/reader?book=${encodeURIComponent(book.b2_key)}`;
    };

    card.innerHTML = `
      <div class="cover-container">
        <img src="${book.cover_url}" alt="${book.title}" onerror="this.src='https://via.placeholder.com/200x280?text=No+Cover'">
      </div>
      <div class="book-info">
        <h3>${book.title}</h3>
        <p>By ${book.author}</p>
        <span class="category-badge">${book.category_name || 'Uncategorized'}</span>
      </div>
    `;
    catalog.appendChild(card);
  });
}

function filterCategory(catId, btnElement) {
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  btnElement.classList.add('active');

  if (catId === 'all') {
    renderBooks(allBooks);
  } else {
    const filtered = allBooks.filter(book => book.category_id === catId);
    renderBooks(filtered);
  }
}

document.addEventListener('DOMContentLoaded', initLibrary);
