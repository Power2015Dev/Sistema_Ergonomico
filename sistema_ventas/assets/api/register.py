from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
import psycopg2
from db import Connect as obtener_conexion

register_bp = Blueprint('register', __name__)

@register_bp.route('/api/register', methods=['POST'])
def registrar_usuario():

    datos = request.json
    
    
    if not datos or not all([datos.get('nombre'), datos.get('apellido'), datos.get('email'), datos.get('password'), datos.get('rol')]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

  
    password_encriptada = generate_password_hash(datos['password'])

    conexion = None
    cursor = None
    try:

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        query = """
            INSERT INTO usuarios (nombre, apellido, email, password_hash, rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario, nombre, email;
        """
        

        valores = (
            datos['nombre'],
            datos['apellido'],
            datos['email'],
            password_encriptada,
            datos['rol']
        )

   
        cursor.execute(query, valores)
        nuevo_usuario = cursor.fetchone()

        conexion.commit() 

  
        return jsonify({
            "mensaje": "Usuario creado exitosamente",
            "datos_guardados": {
                "id": nuevo_usuario[0],
                "nombre": nuevo_usuario[1],
                "email": nuevo_usuario[2]
            }
        }), 201

    except psycopg2.errors.UniqueViolation:
  
        if conexion:
            conexion.rollback()
        return jsonify({"error": "Este correo ya está registrado"}), 409
        
    except Exception as error:
    
        if conexion:
            conexion.rollback()
        return jsonify({"error": f"Ocurrió un error en el servidor: {str(error)}"}), 500
        
    finally:
   
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()