from flask import Blueprint, jsonify
from db import Connect

direcciones_bp = Blueprint('direcciones', __name__)

@direcciones_bp.route('/api/get_direcciones', methods=['GET'])
def obtener_direcciones():
    conexion = None
    cursor = None
    try:
        
        conexion = Connect()
        cursor = conexion.cursor()

    
        query = """
            SELECT id_direccion, id_cliente, calle_numero, ciudad, 
                   estado_provincia, codigo_postal, es_principal
            FROM direcciones
            ORDER BY id_cliente ASC, es_principal DESC;
        """
        cursor.execute(query)
        direcciones_db = cursor.fetchall()

       
        lista_direcciones = []
        for fila in direcciones_db:
            direccion = {
                "id_direccion": fila[0],
                "id_cliente": fila[1],
                "calle_numero": fila[2],
                "ciudad": fila[3],
                "estado_provincia": fila[4],
                "codigo_postal": fila[5],
                "es_principal": fila[6]
            }
            lista_direcciones.append(direccion)


        return jsonify({
            "mensaje": "Direcciones obtenidas correctamente",
            "total_direcciones": len(lista_direcciones),
            "data": lista_direcciones
        }), 200

    except Exception as error:
        return jsonify({"error": f"Error al obtener las direcciones: {str(error)}"}), 500
        
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()