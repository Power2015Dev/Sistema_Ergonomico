from flask import Flask, send_from_directory
from flask_cors import CORS

from assets.api.login import login_bp
from assets.api.register import register_bp
from assets.api.productos import productos_bp
from assets.api.direccion import direcciones_bp
from assets.api.register_cliente import register_cliente_bp
from assets.api.login_cliente import login_cliente_bp
from assets.api.publish_productos import publish_productos_bp
from assets.api.pedidos import pedidos_bp
from assets.api.detalle_pedido import detalle_pedido_bp
from assets.api.actualizar_producto import actualizar_producto_bp
from assets.api.eliminar_producto import eliminar_producto_bp

app = Flask(__name__)
CORS(app)  # Habilitar CORS para que el frontend pueda hacer fetch()

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(direcciones_bp)
app.register_blueprint(register_cliente_bp)
app.register_blueprint(login_cliente_bp)
app.register_blueprint(publish_productos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalle_pedido_bp)
app.register_blueprint(actualizar_producto_bp)
app.register_blueprint(eliminar_producto_bp)


# ═══════════════════════════════════════════════
# Servir archivos estáticos del frontend
# Para que todo funcione desde http://localhost:5000
# ═══════════════════════════════════════════════

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filepath>')
def serve_static(filepath):
    """Sirve cualquier archivo estático (HTML, CSS, JS, imágenes)"""
    return send_from_directory('.', filepath)


if __name__ == '__main__':
    app.run(debug=True)