import shutil
import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Imágenes generadas por IA
imagenes_ia = {
    "silla": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\b418e906-3981-499c-ac8d-2d24ca09995e\ergo_chair_premium_1783352860773.png",
    "escritorio": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\b418e906-3981-499c-ac8d-2d24ca09995e\standing_desk_wood_1783352877310.png",
    "brazo": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\b418e906-3981-499c-ac8d-2d24ca09995e\monitor_arm_dual_1783352887033.png",
    "reposapies": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\b418e906-3981-499c-ac8d-2d24ca09995e\ergo_footrest_1783352895215.png",
    "mouse": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\b418e906-3981-499c-ac8d-2d24ca09995e\ergo_mouse_1783355698837.png",
    "teclado": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\b418e906-3981-499c-ac8d-2d24ca09995e\ergo_keyboard_1783355706462.png",
    "laptop_stand": r"C:\Users\EQUIPO DELL\.gemini\antigravity\brain\b418e906-3981-499c-ac8d-2d24ca09995e\laptop_stand_1783355713696.png"
}

destinos = {
    "silla": "assets/images/ai_chair.png",
    "escritorio": "assets/images/ai_desk.png",
    "brazo": "assets/images/ai_arm.png",
    "reposapies": "assets/images/ai_footrest.png",
    "mouse": "assets/images/ai_mouse.png",
    "teclado": "assets/images/ai_keyboard.png",
    "laptop_stand": "assets/images/ai_laptop_stand.png"
}

# 1. Copiar las imágenes
print("Copiando imágenes generadas por IA a assets/images/...")
os.makedirs("assets/images", exist_ok=True)
for key, src in imagenes_ia.items():
    try:
        shutil.copy(src, destinos[key])
        print(f"✅ {key} copiada con éxito.")
    except Exception as e:
        print(f"❌ Error al copiar {key}: {e}")

# 2. Insertar en la Base de Datos
productos = [
    (1, 'AI-CHAIR-PRO', 'Silla Ergonómica Pro Max AI', 'Soporte lumbar dinámico y malla ultra transpirable.', 'Diseñada para quienes pasan más de 8 horas frente a la PC. Cuenta con brazos 4D, mecanismo sincrónico y cabezal ajustable.', 399.99, 349.99, 25, '../' + destinos['silla'], True, True),
    (1, 'AI-DESK-ELITE', 'Escritorio Motorizado Nogal', 'Ajuste de altura silencioso con top de madera sólida.', 'Superficie de nogal natural de 140x70cm. Panel de memoria de 4 posiciones con sensores anticolisión y carga USB integrada.', 599.00, None, 10, '../' + destinos['escritorio'], True, True),
    (1, 'AI-ARM-DUAL', 'Brazo Monitor Dual Gas Spring', 'Soporte de aluminio para dos monitores de hasta 32".', 'Libera espacio en tu escritorio con este brazo articulado. Gestión de cables oculta y rotación 360° para modo retrato/paisaje.', 129.50, 99.00, 50, '../' + destinos['brazo'], True, False),
    (1, 'AI-FOOT-REST', 'Reposapiés ErgoComfort', 'Ángulo ajustable con textura masajeadora.', 'Mejora la circulación y corrige la postura de tu espalda baja al instante. Superficie de goma antideslizante lavable.', 55.00, None, 100, '../' + destinos['reposapies'], True, False),
    (1, 'AI-MOUSE-VERT', 'Mouse Vertical Inalámbrico Pro', 'Previene el túnel carpiano con agarre natural a 57°.', 'Diseño ergonómico comprobado que reduce la tensión muscular en el antebrazo. Conexión Bluetooth 5.0 y batería recargable.', 89.99, 75.00, 45, '../' + destinos['mouse'], True, True),
    (1, 'AI-KEYBOARD-SPLIT', 'Teclado Mecánico Dividido', 'Postura natural de las manos con switches silenciosos.', 'Teclado curvado en 3D con reposamuñecas acolchado. Alivia la presión en las muñecas y permite escribir durante horas sin fatiga.', 149.00, None, 30, '../' + destinos['teclado'], True, False),
    (1, 'AI-LAPTOP-STAND', 'Soporte Premium para Laptop', 'Aluminio aeroespacial para elevación ergonómica.', 'Eleva tu laptop al nivel de los ojos para evitar el dolor de cuello. Diseño abierto para máxima ventilación y topes antideslizantes.', 45.00, 35.00, 120, '../' + destinos['laptop_stand'], True, False)
]

try:
    print("\nConectando a PostgreSQL...")
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )
    cursor = conn.cursor()

    for p in productos:
        cursor.execute("""
            INSERT INTO productos (id_categoria, sku, nombre, descripcion_corta, descripcion_larga, precio, precio_descuento, stock, imagen_url, estado, es_destacado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sku) DO NOTHING;
        """, p)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ ¡Productos insertados en la base de datos correctamente!")
except Exception as e:
    print(f"❌ Error en la base de datos: {e}")
