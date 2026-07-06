from flask import Blueprint, jsonify
from db import Connect


productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/api/get_productos', methods=['GET'])
def obtener_productos():
    conexion = None
    cursor = None
    try:
        
        conexion = Connect()
        cursor = conexion.cursor()

        
        query = """
            SELECT id_producto, id_categoria, sku, nombre, descripcion_corta, 
                   descripcion_larga, precio, precio_descuento, stock, 
                   imagen_url, estado, es_destacado
            FROM productos
            ORDER BY id_producto ASC;
        """
        cursor.execute(query)
        
     
        productos_db = cursor.fetchall()

   
        lista_productos = []
        for fila in productos_db:
            producto = {
                "id_producto": fila[0],
                "id_categoria": fila[1],
                "sku": fila[2],
                "nombre": fila[3],
                "descripcion_corta": fila[4],
                "descripcion_larga": fila[5],

                "precio": float(fila[6]) if fila[6] is not None else 0.00,
                "precio_descuento": float(fila[7]) if fila[7] is not None else None,
                "stock": fila[8],
                "imagen_url": fila[9],
                "estado": fila[10],
                "es_destacado": fila[11]
            }
            lista_productos.append(producto)


        return jsonify({
            "mensaje": "Productos obtenidos correctamente",
            "total_productos": len(lista_productos),
            "data": lista_productos
        }), 200

    except Exception as error:
        return jsonify({"error": f"Error al obtener los productos: {str(error)}"}), 500
        
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()