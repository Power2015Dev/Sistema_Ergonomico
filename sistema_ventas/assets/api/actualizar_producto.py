from flask import Blueprint, request, jsonify
from db import Connect

actualizar_producto_bp = Blueprint('actualizar_producto', __name__)

@actualizar_producto_bp.route('/api/actualizar_producto/<int:id_producto>', methods=['PUT', 'POST'])
def actualizar_producto(id_producto):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    try:
        con = Connect()
        cursor = con.cursor()
        
        # Verificar si existe
        cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (id_producto,))
        if not cursor.fetchone():
            return jsonify({"error": "Producto no encontrado"}), 404

        # Actualizar
        query = """
            UPDATE productos 
            SET id_categoria = %s, sku = %s, nombre = %s, descripcion_corta = %s, 
                descripcion_larga = %s, precio = %s, precio_descuento = %s, 
                stock = %s, imagen_url = %s, estado = %s
            WHERE id_producto = %s
        """
        valores = (
            data.get('id_categoria'),
            data.get('sku'),
            data.get('nombre'),
            data.get('descripcion_corta'),
            data.get('descripcion_larga'),
            data.get('precio'),
            data.get('precio_descuento'),
            data.get('stock'),
            data.get('imagen_url'),
            data.get('estado', True),
            id_producto
        )
        
        cursor.execute(query, valores)
        con.commit()
        
        return jsonify({"message": "Producto actualizado correctamente"}), 200

    except Exception as e:
        if con:
            con.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
