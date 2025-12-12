#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/fix_acudientes_aspirantes.py

Script para agregar usuarios a los acudientes de aspirantes que no tienen usuario.
"""

import sys
import os
from pathlib import Path

# Configurar salida UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.data.db import engine
from sqlalchemy import text
import bcrypt

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def fix_acudientes():
    """Agrega usuarios a los acudientes sin usuario"""
    
    print("=" * 80)
    print("AGREGANDO USUARIOS A ACUDIENTES DE ASPIRANTES")
    print("=" * 80)
    
    credenciales = []
    
    with engine.connect() as conn:
        trans = conn.begin()
        
        try:
            # Obtener id_rol de acudiente
            rol_acudiente = conn.execute(
                text("SELECT id_rol FROM rol WHERE nombre_rol = 'acudiente'")
            ).fetchone()
            
            if not rol_acudiente:
                print("❌ Error: No se encontró el rol 'acudiente'")
                return
            
            id_rol_acudiente = rol_acudiente[0]
            print(f"✓ Rol acudiente encontrado: ID {id_rol_acudiente}\n")
            
            # Buscar acudientes sin usuario
            acudientes_sin_usuario = conn.execute(
                text("""
                    SELECT 
                        a.id_acudiente,
                        p.tipo_identificacion,
                        p.numero_identificacion,
                        p.primer_nombre,
                        p.segundo_nombre,
                        p.primer_apellido,
                        p.segundo_apellido,
                        p.telefono,
                        a.parentesco
                    FROM acudiente a
                    JOIN persona p ON a.id_acudiente = p.id_persona
                    WHERE a.id_usuario IS NULL
                """)
            ).fetchall()
            
            if not acudientes_sin_usuario:
                print("✓ No hay acudientes sin usuario\n")
                return
            
            print(f"Encontrados {len(acudientes_sin_usuario)} acudientes sin usuario:\n")
            
            # Datos de emails para los acudientes (basados en los que definimos en populate_database)
            emails_acudientes = {
                "1090909090": "torres.felipe@gmail.com",
                "1091919191": "carolina.mejia@hotmail.com",
                "1092929292": "ricardo.castro@yahoo.com"
            }
            
            for acud in acudientes_sin_usuario:
                id_acudiente = acud[0]
                cedula = acud[2]
                primer_nombre = acud[3]
                segundo_nombre = acud[4]
                primer_apellido = acud[5]
                segundo_apellido = acud[6]
                parentesco = acud[8]
                
                nombre_completo = f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}".strip()
                
                # Obtener email
                email = emails_acudientes.get(cedula)
                if not email:
                    print(f"  ⚠️  No se encontró email para cédula {cedula}, omitiendo...")
                    continue
                
                # Verificar si el email ya existe
                existe_email = conn.execute(
                    text("SELECT id_usuario FROM usuario WHERE correo_electronico = :email"),
                    {"email": email}
                ).fetchone()
                
                if existe_email:
                    print(f"  ⚠️  Email {email} ya existe, omitiendo...")
                    continue
                
                # Generar contraseña
                password = f"acud{cedula[-4:]}"
                
                # Crear usuario
                id_usuario = conn.execute(
                    text("""
                        INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo)
                        VALUES (:email, :pwd, :rol, true)
                        RETURNING id_usuario
                    """),
                    {
                        "email": email,
                        "pwd": hash_password(password),
                        "rol": id_rol_acudiente
                    }
                ).fetchone()[0]
                
                # Actualizar acudiente con el id_usuario
                conn.execute(
                    text("""
                        UPDATE acudiente 
                        SET id_usuario = :id_usuario 
                        WHERE id_acudiente = :id_acudiente
                    """),
                    {
                        "id_usuario": id_usuario,
                        "id_acudiente": id_acudiente
                    }
                )
                
                print(f"  ✅ Usuario creado: {nombre_completo} ({email}) - Cédula: {cedula}")
                
                credenciales.append({
                    'rol': 'Acudiente',
                    'nombre': nombre_completo,
                    'email': email,
                    'password': password,
                    'cedula': cedula
                })
            
            # Confirmar transacción
            trans.commit()
            
            print("\n" + "=" * 80)
            print("✅ USUARIOS AGREGADOS EXITOSAMENTE")
            print("=" * 80)
            
            # Guardar credenciales
            if credenciales:
                log_path = project_root / "logs" / "credenciales_usuarios.txt"
                
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write("\n" + "=" * 80 + "\n")
                    f.write("ACUDIENTES DE ASPIRANTES - USUARIOS AGREGADOS\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for cred in credenciales:
                        f.write(f"Rol: {cred['rol']}\n")
                        f.write(f"Nombre: {cred['nombre']}\n")
                        f.write(f"Email: {cred['email']}\n")
                        f.write(f"Contraseña: {cred['password']}\n")
                        f.write(f"Cédula: {cred['cedula']}\n")
                        f.write("-" * 40 + "\n\n")
                
                print(f"\n✅ Credenciales guardadas en: {log_path}")
                print(f"\n📊 Total usuarios creados: {len(credenciales)}")
            
        except Exception as e:
            trans.rollback()
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    try:
        fix_acudientes()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
        sys.exit(1)
