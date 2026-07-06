/* ═══════════════════════════════════════════════════
   API.JS — Módulo central de conexión Frontend ↔ Backend
   ErgoVida — Sistema Ergonómico
   ═══════════════════════════════════════════════════ */

const API_BASE = 'http://localhost:5000';

// ─── Función base para todas las peticiones ───
async function apiRequest(endpoint, options = {}) {
    try {
        const config = {
            headers: { 'Content-Type': 'application/json' },
            ...options
        };
        const response = await fetch(API_BASE + endpoint, config);
        const data = await response.json();
        if (!response.ok) {
            throw { status: response.status, ...data };
        }
        return data;
    } catch (error) {
        if (error.status) throw error;
        console.error('Error de conexión:', error);
        throw { error: 'No se pudo conectar con el servidor. Verifica que Flask esté corriendo.' };
    }
}

// ═══════════════════════════════════════
// API — Llamadas al backend
// ═══════════════════════════════════════
const API = {
    // ── Auth Clientes ──
    loginCliente(email, password) {
        return apiRequest('/api/clientes/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },
    registerCliente(data) {
        return apiRequest('/api/clientes/register', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // ── Auth Admin/Usuarios ──
    loginAdmin(email, password) {
        return apiRequest('/api/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },
    registerAdmin(data) {
        return apiRequest('/api/register', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // ── Productos ──
    getProductos() {
        return apiRequest('/api/get_productos');
    },
    ingresarProducto(data) {
        return apiRequest('/api/ingresar_producto', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    actualizarProducto(id, data) {
        return apiRequest('/api/actualizar_producto/' + id, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    eliminarProducto(id) {
        return apiRequest('/api/eliminar_producto/' + id, {
            method: 'DELETE'
        });
    },

    // ── Pedidos ──
    getPedidos() {
        return apiRequest('/api/get_pedidos');
    },
    insertarPedido(data) {
        return apiRequest('/api/insertar_pedido', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // ── Detalle Pedido ──
    getDetalles() {
        return apiRequest('/api/get_detalles');
    },
    insertarDetalle(data) {
        return apiRequest('/api/insertar_detalle', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // ── Direcciones ──
    getDirecciones() {
        return apiRequest('/api/get_direcciones');
    }
};

// ═══════════════════════════════════════
// SESSION — Manejo de sesión con localStorage
// ═══════════════════════════════════════
const Session = {
    _key: 'ergovida_session',

    set(tipo, datos) {
        const session = { tipo, ...datos, timestamp: Date.now() };
        localStorage.setItem(this._key, JSON.stringify(session));
    },

    get() {
        const s = localStorage.getItem(this._key);
        return s ? JSON.parse(s) : null;
    },

    clear() {
        localStorage.removeItem(this._key);
    },

    isLoggedIn() {
        return this.get() !== null;
    },

    isAdmin() {
        const s = this.get();
        return s && s.tipo === 'admin' && s.usuario && s.usuario.rol === 'admin';
    },

    isVendedor() {
        const s = this.get();
        return s && s.tipo === 'admin' && s.usuario && s.usuario.rol === 'vendedor';
    },

    isCliente() {
        const s = this.get();
        return s && s.tipo === 'cliente';
    },

    getUserName() {
        const s = this.get();
        if (!s) return 'Invitado';
        if (s.tipo === 'admin') return s.usuario.nombre + ' ' + s.usuario.apellido;
        return s.cliente.nombre_completo;
    },

    getUserId() {
        const s = this.get();
        if (!s) return null;
        if (s.tipo === 'admin') return s.usuario.id;
        return s.cliente.id;
    },

    requireAuth(redirectTo) {
        if (!this.isLoggedIn()) {
            window.location.href = redirectTo || '../pages/login.html';
            return false;
        }
        return true;
    },

    requireAdmin(redirectTo) {
        if (!this.isAdmin()) {
            window.location.href = redirectTo || '../pages/login.html';
            return false;
        }
        return true;
    }
};

// ═══════════════════════════════════════
// CARRITO — Carrito de compras con localStorage
// ═══════════════════════════════════════
const Carrito = {
    _key: 'ergovida_carrito',

    getItems() {
        return JSON.parse(localStorage.getItem(this._key) || '[]');
    },

    _save(items) {
        localStorage.setItem(this._key, JSON.stringify(items));
        this.updateUI();
    },

    addItem(producto, cantidad = 1) {
        const items = this.getItems();
        const idx = items.findIndex(i => i.id_producto === producto.id_producto);
        if (idx >= 0) {
            items[idx].cantidad += cantidad;
        } else {
            items.push({
                id_producto: producto.id_producto,
                nombre: producto.nombre,
                precio: parseFloat(producto.precio),
                precio_descuento: producto.precio_descuento ? parseFloat(producto.precio_descuento) : null,
                imagen_url: producto.imagen_url,
                descripcion_corta: producto.descripcion_corta || '',
                cantidad: cantidad
            });
        }
        this._save(items);
        return true;
    },

    removeItem(id_producto) {
        const items = this.getItems().filter(i => i.id_producto !== id_producto);
        this._save(items);
    },

    updateQty(id_producto, cantidad) {
        const items = this.getItems();
        const item = items.find(i => i.id_producto === id_producto);
        if (item) {
            item.cantidad = Math.max(1, parseInt(cantidad));
            this._save(items);
        }
    },

    getPrecio(item) {
        return item.precio_descuento || item.precio;
    },

    getSubtotal() {
        return this.getItems().reduce((sum, i) => sum + (this.getPrecio(i) * i.cantidad), 0);
    },

    getImpuestos(rate = 0.16) {
        return this.getSubtotal() * rate;
    },

    getTotal() {
        return this.getSubtotal() + this.getImpuestos();
    },

    getCount() {
        return this.getItems().reduce((sum, i) => sum + i.cantidad, 0);
    },

    clear() {
        localStorage.removeItem(this._key);
        this.updateUI();
    },

    updateUI() {
        document.querySelectorAll('.carrito-count').forEach(el => {
            const count = this.getCount();
            el.textContent = count;
            el.style.display = count > 0 ? '' : 'none';
        });
    }
};

// ═══════════════════════════════════════
// TOAST — Notificaciones
// ═══════════════════════════════════════
function showToast(type, message, duration = 3500) {
    let container = document.getElementById('toasts');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toasts';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// ═══════════════════════════════════════
// UTILS — Utilidades comunes
// ═══════════════════════════════════════
function formatPrice(num) {
    return '$' + parseFloat(num).toFixed(2);
}

function generateOrderCode() {
    return 'PED-' + Date.now().toString(36).toUpperCase();
}

// Inicializar badges del carrito al cargar cualquier página
document.addEventListener('DOMContentLoaded', () => {
    Carrito.updateUI();
});
