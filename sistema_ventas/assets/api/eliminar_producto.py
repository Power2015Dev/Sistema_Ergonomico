from flask import Blueprint, request, jsonify
from db import Connect

eliminar_producto_bp = Blueprint('eliminar_producto', __name__)

@eliminar_producto_bp.route('/api/eliminar_producto/<int:id_producto>', methods=['DELETE', 'POST'])
def eliminar_producto(id_producto):
    try:
        con = Connect()
        cursor = con.cursor()
        
        # Primero verificar si el producto tiene detalles de pedido asociados
        # Si los tiene, no se puede eliminar físicamente, se debe cambiar el estado a "inactivo"
        cursor.execute("SELECT id_detalle FROM detalle_pedido WHERE id_producto = %s LIMIT 1", (id_producto,))
        if cursor.fetchone():
            cursor.execute("UPDATE productos SET estado = false, stock = 0 WHERE id_producto = %s", (id_producto,))
            con.commit()
            return jsonify({"message": "El producto tiene pedidos asociados. Se ha ocultado del catálogo en lugar de eliminarse."}), 200

        # Si no tiene historial, se elimina permanentemente
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Producto no encontrado"}), 404
            
        con.commit()
        return jsonify({"message": "Producto eliminado permanentemente"}), 200

    except Exception as e:
        if con:
            con.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
