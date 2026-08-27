document.addEventListener('DOMContentLoaded', async () => {
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  if (!input || !results) return;

  let index = [];
  try {
    const res = await fetch(input.dataset.indexPath || 'assets/js/search-index.json');
    if (res.ok) index = await res.json();
  } catch (e) {
    console.error('Error loading search index', e);
  }

  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    if (q.length < 2) {
      results.style.display = 'none';
      results.innerHTML = '';
      return;
    }

    const matches = index.filter(item => 
      item.title.toLowerCase().includes(q) || 
      item.profession.toLowerCase().includes(q) || 
      item.country.toLowerCase().includes(q)
    ).slice(0, 10);

    if (matches.length === 0) {
      results.innerHTML = '<div style="padding: 16px; color: #94a3b8; text-align: center;">No se encontraron guías para esa búsqueda.</div>';
      results.style.display = 'block';
      return;
    }

    results.innerHTML = matches.map(m => `
      <a href="${m.url}" class="search-result-item">
        <div>
          <strong style="color: #fff;">${m.title}</strong>
          <div style="font-size: 0.8rem; color: #94a3b8;">${m.profession} &bull; ${m.country}</div>
        </div>
        <span style="color: #10b981; font-weight: 700;">Ver tarifa &rarr;</span>
      </a>
    `).join('');
    results.style.display = 'block';
  });

  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.style.display = 'none';
    }
  });
});