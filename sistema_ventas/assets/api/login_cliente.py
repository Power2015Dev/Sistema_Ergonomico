from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
import psycopg2
from db import Connect


login_cliente_bp = Blueprint('login_cliente', __name__)

@login_cliente_bp.route('/api/clientes/login', methods=['POST'])
def iniciar_sesion_cliente():
    datos = request.json
    
    if not datos or not datos.get('email') or not datos.get('password'):
        return jsonify({"error": "El correo y la contraseña son obligatorios"}), 400

    conexion = None
    cursor = None
    try:
        conexion = Connect()
        cursor = conexion.cursor()
        

        query = """
            SELECT id_cliente, nombre_completo, password_hash, telefono, estado 
            FROM clientes 
            WHERE email = %s
        """
        cursor.execute(query, (datos['email'],))
        cliente_db = cursor.fetchone()
        
        if not cliente_db:
            return jsonify({"error": "Credenciales inválidas"}), 401
            
        id_cliente, nombre_completo, hash_guardado, telefono, estado = cliente_db
        
      
        if not estado:
            return jsonify({"error": "Su cuenta está suspendida. Contacte a soporte."}), 403


        if check_password_hash(hash_guardado, datos['password']):
            return jsonify({
                "mensaje": "Inicio de sesión exitoso. Puede proceder al pago.",
                "cliente": {
                    "id": id_cliente,
                    "nombre_completo": nombre_completo,
                    "email": datos['email'],
                    "telefono": telefono
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as error:
        return jsonify({"error": f"Error en el servidor: {str(error)}"}), 500
        
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()