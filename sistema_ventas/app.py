from flask import Flask

from assets.api.login import login_bp
from assets.api.register import register_bp
from assets.api.productos import productos_bp
from assets.api.direccion import direcciones_bp
from assets.api.register_cliente import register_cliente_bp
from assets.api.login_cliente import login_cliente_bp
from assets.api.publish_productos import publish_productos_bp
from assets.api.pedidos import pedidos_bp
from assets.api.detalle_pedido import detalle_pedido_bp
app = Flask(__name__)


app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(direcciones_bp)
app.register_blueprint(register_cliente_bp)
app.register_blueprint(login_cliente_bp)
app.register_blueprint(publish_productos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalle_pedido_bp)



@app.route('/')
def home():
    return "Servidor principal funcionando"

if __name__ == '__main__':
    app.run(debug=True)