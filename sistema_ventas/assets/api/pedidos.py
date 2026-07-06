from flask import Blueprint, jsonify, request
import psycopg2
from db import Connect

pedidos_bp = Blueprint('pedidos', __name__)


@pedidos_bp.route('/api/get_pedidos', methods=['GET'])
def obtener_pedidos():
    conexion = None
    cursor = None
    try:
        conexion = Connect()
        cursor = conexion.cursor()

        query = """
            SELECT id_pedido, codigo_pedido, id_cliente, id_direccion, 
                   total, estado_pago, estado_envio, metodo_pago, fecha_pedido
            FROM pedidos
            ORDER BY fecha_pedido DESC;
        """
        cursor.execute(query)
        pedidos_db = cursor.fetchall()

        lista_pedidos = []
        for fila in pedidos_db:
            pedido = {
                "id_pedido": fila[0],
                "codigo_pedido": fila[1],
                "id_cliente": fila[2],
                "id_direccion": fila[3],
                "total": float(fila[4]),
                "estado_pago": fila[5],
                "estado_envio": fila[6],
                "metodo_pago": fila[7],
                "fecha_pedido": fila[8].strftime('%Y-%m-%d %H:%M:%S') if fila[8] else None
            }
            lista_pedidos.append(pedido)

        return jsonify({
            "mensaje": "Pedidos obtenidos correctamente",
            "total_pedidos": len(lista_pedidos),
            "data": lista_pedidos
        }), 200

    except Exception as error:
        return jsonify({"error": f"Error: {str(error)}"}), 500
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()


@pedidos_bp.route('/api/insertar_pedido', methods=['POST'])
def insertar_pedido():
    datos = request.json

  
    campos_req = ['codigo_pedido', 'id_cliente', 'id_direccion', 'total', 'metodo_pago']
    if not datos or not all(campo in datos for campo in campos_req):
        return jsonify({"error": "Faltan datos obligatorios para crear el pedido"}), 400

    conexion = None
    cursor = None
    try:
        conexion = Connect()
        cursor = conexion.cursor()

        query = """
            INSERT INTO pedidos (codigo_pedido, id_cliente, id_direccion, total, estado_pago, estado_envio, metodo_pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_pedido, codigo_pedido;
        """
  
        valores = (
            datos['codigo_pedido'],
            datos['id_cliente'],
            datos['id_direccion'],
            datos['total'],
            datos.get('estado_pago', 'pendiente'),
            datos.get('estado_envio', 'pendiente'),
            datos['metodo_pago']
        )

        cursor.execute(query, valores)
        nuevo_pedido = cursor.fetchone()
        conexion.commit()

        return jsonify({
            "mensaje": "Pedido registrado exitosamente",
            "pedido": {
                "id_pedido": nuevo_pedido[0],
                "codigo_pedido": nuevo_pedido[1]
            }
        }), 201

    except psycopg2.errors.UniqueViolation:
        if conexion: conexion.rollback()
        return jsonify({"error": "Ese código de pedido ya existe en el sistema."}), 409
        
    except psycopg2.errors.ForeignKeyViolation as fk_error:

        if conexion: conexion.rollback()
        return jsonify({
            "error": "Error de relación: El cliente o la dirección indicados no existen en la base de datos.",
            "detalle_tecnico": str(fk_error)
        }), 400

    except Exception as error:
        if conexion: conexion.rollback()
        return jsonify({"error": f"Error en el servidor: {str(error)}"}), 500
        
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()