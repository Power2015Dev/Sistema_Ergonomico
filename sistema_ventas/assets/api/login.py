from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
import psycopg2
from db import Connect

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def iniciar_sesion():
 
    datos = request.json
    

    if not datos or not datos.get('email') or not datos.get('password'):
        return jsonify({"error": "El correo y la contraseña son obligatorios"}), 400

    conexion = None
    cursor = None
    try:
    
        conexion = Connect()
        cursor = conexion.cursor()
        

        query = """
            SELECT id_usuario, nombre, apellido, password_hash, rol, estado 
            FROM usuarios 
            WHERE email = %s
        """
        cursor.execute(query, (datos['email'],))
        usuario_db = cursor.fetchone()
        
  
        if not usuario_db:
        
            return jsonify({"error": "Credenciales inválidas"}), 401
            

        id_usuario, nombre, apellido, hash_guardado, rol, estado = usuario_db
        
        if not estado:
            return jsonify({"error": "Esta cuenta está desactivada. Contacte al administrador."}), 403

        
        if check_password_hash(hash_guardado, datos['password']):
            
       
            return jsonify({
                "mensaje": "Inicio de sesión exitoso",
                "usuario": {
                    "id": id_usuario,
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": datos['email'],
                    "rol": rol
                }
            }), 200
        else:
   
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as error:
        return jsonify({"error": f"Ocurrió un error en el servidor: {str(error)}"}), 500
        
    finally:
   
        if cursor: 
            cursor.close()
        if conexion: 
            conexion.close()