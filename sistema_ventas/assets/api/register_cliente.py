from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
import psycopg2
from db import Connect


register_cliente_bp = Blueprint('register_cliente', __name__)

@register_cliente_bp.route('/api/clientes/register', methods=['POST'])
def registrar_cliente():
    datos = request.json
    

    if not datos or not all([datos.get('nombre_completo'), datos.get('email'), datos.get('password')]):
        return jsonify({"error": "Faltan datos obligatorios (nombre, email o contraseña)"}), 400


    password_encriptada = generate_password_hash(datos['password'])
    

    telefono = datos.get('telefono', None)

    conexion = None
    cursor = None
    try:
        conexion = Connect()
        cursor = conexion.cursor()


        query = """
            INSERT INTO clientes (nombre_completo, email, password_hash, telefono)
            VALUES (%s, %s, %s, %s)
            RETURNING id_cliente, nombre_completo, email;
        """
        
        valores = (datos['nombre_completo'], datos['email'], password_encriptada, telefono)

        cursor.execute(query, valores)
        nuevo_cliente = cursor.fetchone()
        conexion.commit() 

        return jsonify({
            "mensaje": "Cuenta de cliente creada exitosamente. ¡Bienvenido a la tienda!",
            "datos_guardados": {
                "id": nuevo_cliente[0],
                "nombre_completo": nuevo_cliente[1],
                "email": nuevo_cliente[2]
            }
        }), 201

    except psycopg2.errors.UniqueViolation:
        if conexion:
            conexion.rollback()
        return jsonify({"error": "Este correo ya está registrado. Por favor, inicie sesión."}), 409
        
    except Exception as error:
        if conexion:
            conexion.rollback()
        return jsonify({"error": f"Error en el servidor: {str(error)}"}), 500
        
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()