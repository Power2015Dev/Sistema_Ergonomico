from flask import Blueprint, jsonify, request
import psycopg2
from db import Connect

publish_productos_bp = Blueprint('publish_productos_bp', __name__)

@publish_productos_bp.route('/api/ingresar_producto', methods=['POST'])
def insertar_producto():
    datos = request.json


    campos_obligatorios = ['id_categoria', 'sku', 'nombre', 'precio', 'stock']
    if not datos or not all(campo in datos for campo in campos_obligatorios):
        return jsonify({"error": "Faltan datos obligatorios (id_categoria, sku, nombre, precio, stock)"}), 400

    conexion = None
    cursor = None
    try:
        conexion = Connect()
        cursor = conexion.cursor()


        query = """
            INSERT INTO productos (
                id_categoria, sku, nombre, descripcion_corta, descripcion_larga, 
                precio, precio_descuento, stock, imagen_url, estado, es_destacado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_producto, nombre;
        """

       
        valores = (
            datos['id_categoria'],
            datos['sku'],
            datos['nombre'],
            datos.get('descripcion_corta', None),
            datos.get('descripcion_larga', None),
            datos['precio'],
            datos.get('precio_descuento', None),
            datos['stock'],
            datos.get('imagen_url', None),
            datos.get('estado', True),          
            datos.get('es_destacado', False)    
        )


        cursor.execute(query, valores)
        nuevo_producto = cursor.fetchone()
        conexion.commit()

        return jsonify({
            "mensaje": "Producto registrado exitosamente en el catálogo",
            "producto": {
                "id_producto": nuevo_producto[0],
                "nombre": nuevo_producto[1]
            }
        }), 201

    except psycopg2.errors.UniqueViolation:
  
        if conexion: conexion.rollback()
        return jsonify({"error": "El SKU (código de producto) ya existe en la base de datos"}), 409
        
    except psycopg2.errors.ForeignKeyViolation:
      
        if conexion: conexion.rollback()
        return jsonify({"error": "La categoría asignada no existe"}), 400

    except Exception as error:
        if conexion: conexion.rollback()
        return jsonify({"error": f"Error en el servidor: {str(error)}"}), 500
        
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()