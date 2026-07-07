import shutil
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Rutas de las imágenes generadas por la IA
imagenes_ia = {
    "silla": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\11e11615-71de-445f-8f68-3f9556a94eda\silla_pro_1783389167025.png",
    "escritorio": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\11e11615-71de-445f-8f68-3f9556a94eda\escritorio_1783389173932.png",
    "soporte": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\11e11615-71de-445f-8f68-3f9556a94eda\soporte_1783389181829.png",
    "accesorios": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\11e11615-71de-445f-8f68-3f9556a94eda\accesorios_1783389189739.png",
    "hero": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\11e11615-71de-445f-8f68-3f9556a94eda\hero_1783389198732.png"
}

destinos = {
    "silla": "assets/images/silla-pro.png",
    "escritorio": "assets/images/escritorio.png",
    "soporte": "assets/images/soporte.png",
    "accesorios": "assets/images/accesorios.png",
    "hero": "assets/images/hero.png"
}

print("1. Copiando imágenes generadas por IA a assets/images/...")
os.makedirs("assets/images", exist_ok=True)
for key, src in imagenes_ia.items():
    try:
        shutil.copy(src, destinos[key])
        print(f"✅ {key} copiada con éxito a {destinos[key]}")
    except Exception as e:
        print(f"❌ Error al copiar {key}: {e}")

print("\n2. Actualizando las imágenes de los productos en la base de datos...")
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )
    cursor = conn.cursor()

    # Actualizar cada producto con una imagen única de acuerdo a su nombre o categoría si es posible
    # O simplemente asignamos las nuevas imágenes a los primeros productos
    
    # Obtener todos los productos
    cursor.execute("SELECT id_producto, nombre FROM productos ORDER BY id_producto ASC")
    productos = cursor.fetchall()
    
    lista_imagenes = [
        "../assets/images/silla-pro.png",
        "../assets/images/escritorio.png",
        "../assets/images/soporte.png",
        "../assets/images/accesorios.png"
    ]
    
    for i, prod in enumerate(productos):
        id_prod = prod[0]
        # Asignar una imagen rotativa de la lista para que no todos tengan la silla
        img_asignada = lista_imagenes[i % len(lista_imagenes)]
        
        cursor.execute("UPDATE productos SET imagen_url = %s WHERE id_producto = %s", (img_asignada, id_prod))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ ¡Imágenes de la base de datos actualizadas con éxito! Ahora cada producto tiene una imagen variada.")
except Exception as e:
    print(f"❌ Error en la base de datos: {e}")
