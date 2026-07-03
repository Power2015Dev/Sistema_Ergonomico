/**
 * admin-sidebar.js
 * Inyecta el sidebar SVG y marca el ítem activo según la página actual.
 * Incluir ANTES del cierre de </body> en cada página admin.
 */
(function () {
  const page = location.pathname.split('/').pop().replace('.html', '');

  const sidebarHTML = `
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round">
          <path d="M20.5 13V7a2 2 0 0 0-2-2h-13a2 2 0 0 0-2 2v6"/>
          <path d="M3 13h18"/><path d="M7 13v6M17 13v6M5 19h14"/>
        </svg>
      </div>
      <div><div class="brand-name">ErgoVida</div><div class="brand-sub">Panel de Gestión</div></div>
    </div>
    <nav class="sidebar-nav">
      <div class="nav-section-label">Principal</div>
      <a class="nav-item" href="dashboard.html" data-page="dashboard">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg></span>
        Dashboard
      </a>
      <div class="nav-section-label">Catálogo</div>
      <a class="nav-item" href="productos.html" data-page="productos">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20.5 13V7a2 2 0 0 0-2-2h-13a2 2 0 0 0-2 2v6"/><path d="M3 13h18"/><path d="M7 13v6M17 13v6M5 19h14"/></svg></span>
        Productos <span class="nav-badge">120</span>
      </a>
      <a class="nav-item" href="categorias.html" data-page="categorias">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></span>
        Categorías
      </a>
      <div class="nav-section-label">Ventas</div>
      <a class="nav-item" href="pedidos.html" data-page="pedidos">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg></span>
        Pedidos <span class="nav-badge">8</span>
      </a>
      <a class="nav-item" href="clientes.html" data-page="clientes">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
        Clientes
      </a>
      <div class="nav-section-label">Sistema</div>
      <a class="nav-item" href="usuarios.html" data-page="usuarios">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></span>
        Usuarios
      </a>
      <a class="nav-item" href="#" data-page="reportes">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></span>
        Reportes
      </a>
      <a class="nav-item" href="#" data-page="configuracion">
        <span class="nav-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>
        Configuración
      </a>
    </nav>
    <div class="sidebar-footer">
      <div class="sidebar-user">
        <div class="avatar">A</div>
        <div><div class="user-name">Administrador</div><div class="user-role">Super Admin</div></div>
        <a href="../pages/login.html" class="logout-btn" title="Salir">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </a>
      </div>
    </div>
  </aside>`;

  // Reemplaza el sidebar existente
  const existing = document.querySelector('.sidebar');
  if (existing) {
    existing.outerHTML = sidebarHTML;
  } else {
    document.querySelector('.admin-layout').insertAdjacentHTML('afterbegin', sidebarHTML);
  }

  // Marca el activo
  document.querySelectorAll('.nav-item[data-page]').forEach(link => {
    if (link.dataset.page === page) link.classList.add('active');
  });

  // Search icon helper
  document.querySelectorAll('.search-bar .icon').forEach(el => {
    if (!el.querySelector('svg')) {
      el.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`;
    }
  });

  // Toast helper global
  window.showToast = function(type, msg) {
    let c = document.getElementById('toasts');
    if (!c) { c = document.createElement('div'); c.id = 'toasts'; c.className = 'toast-container'; document.body.appendChild(c); }
    const t = document.createElement('div');
    t.className = 'toast ' + type;
    t.textContent = msg;
    c.appendChild(t);
    setTimeout(() => t.remove(), 3500);
  };

  // Modal helpers global
  window.abrirModal = id => document.getElementById(id)?.classList.add('active');
  window.cerrarModal = id => document.getElementById(id)?.classList.remove('active');
  document.addEventListener('click', e => {
    if (e.target.classList.contains('modal-overlay')) e.target.classList.remove('active');
    if (e.target.classList.contains('modal-close')) e.target.closest('.modal-overlay')?.classList.remove('active');
  });

  // Filter chips
  document.querySelectorAll('.filter-chip').forEach(c => {
    c.addEventListener('click', function() {
      document.querySelectorAll('.filter-chip').forEach(x => x.classList.remove('active'));
      this.classList.add('active');
    });
  });
})();
