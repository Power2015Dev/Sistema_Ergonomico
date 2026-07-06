from flask import Blueprint, jsonify, request
import psycopg2
from db import Connect

detalle_pedido_bp = Blueprint('detalle_pedido', __name__)


@detalle_pedido_bp.route('/api/get_detalles', methods=['GET'])
def obtener_detalles():
    conexion = None
    cursor = None
    try:
        conexion = Connect()
        cursor = conexion.cursor()

        query = """
            SELECT id_detalle, id_pedido, id_producto, cantidad, 
                   precio_unitario, subtotal
            FROM detalle_pedido
            ORDER BY id_pedido ASC, id_detalle ASC;
        """
        cursor.execute(query)
        detalles_db = cursor.fetchall()

        lista_detalles = []
        for fila in detalles_db:
            detalle = {
                "id_detalle": fila[0],
                "id_pedido": fila[1],
                "id_producto": fila[2],
                "cantidad": fila[3],
                "precio_unitario": float(fila[4]), 
                "subtotal": float(fila[5])       
            }
            lista_detalles.append(detalle)

        return jsonify({
            "mensaje": "Detalles de pedidos obtenidos correctamente",
            "total_registros": len(lista_detalles),
            "data": lista_detalles
        }), 200

    except Exception as error:
        return jsonify({"error": f"Error: {str(error)}"}), 500
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()



@detalle_pedido_bp.route('/api/insertar_detalle', methods=['POST'])
def insertar_detalle():
    datos = request.json

    campos_req = ['id_pedido', 'id_producto', 'cantidad', 'precio_unitario', 'subtotal']
    if not datos or not all(campo in datos for campo in campos_req):
        return jsonify({"error": "Faltan datos obligatorios para agregar el producto al pedido"}), 400

    conexion = None
    cursor = None
    try:
        conexion = Connect()
        cursor = conexion.cursor()

        query = """
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_detalle;
        """
        
        valores = (
            datos['id_pedido'],
            datos['id_producto'],
            datos['cantidad'],
            datos['precio_unitario'],
            datos['subtotal']
        )

        cursor.execute(query, valores)
        nuevo_detalle = cursor.fetchone()
        conexion.commit()

        return jsonify({
            "mensaje": "Producto agregado al pedido exitosamente",
            "id_detalle_generado": nuevo_detalle[0]
        }), 201

    except psycopg2.errors.ForeignKeyViolation:
        if conexion: conexion.rollback()
        return jsonify({
            "error": "Error de relación: El ID del pedido o el ID del producto no existen."
        }), 400

    except Exception as error:
        if conexion: conexion.rollback()
        return jsonify({"error": f"Error en el servidor: {str(error)}"}), 500
        
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()