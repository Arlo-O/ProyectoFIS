from sqlalchemy import text
from app.infraestructura.db import SessionLocal, engine
from app.infraestructura.mappers import start_mappers

print("\n" + "="*60)
print("🌱 CREANDO USUARIO ADMINISTRADOR")
print("="*60 + "\n")

start_mappers()

try:
    session = SessionLocal()
    
    # Verificar si ya existe el admin
    result = session.execute(text("""
        SELECT COUNT(*) FROM usuario 
        WHERE correo_electronico = 'admin@colegio.edu'
    """))
    
    if result.scalar() > 0:
        print("⚠️  El usuario admin@colegio.edu ya existe\n")
        session.close()
        exit(0)
    
    # Crear o usar rol de Administrador
    result = session.execute(text("""
        SELECT id_rol FROM rol WHERE nombre_rol = 'Administrador'
    """))
    rol_row = result.fetchone()
    
    if not rol_row:
        print("1️⃣  Creando rol de Administrador...")
        session.execute(text("""
            INSERT INTO rol (nombre_rol, descripcion_rol)
            VALUES ('Administrador', 'Acceso completo al sistema')
            RETURNING id_rol
        """))
        session.commit()
        
        result = session.execute(text("SELECT id_rol FROM rol WHERE nombre_rol = 'Administrador'"))
        rol_id = result.scalar()
        print(f"   ✅ Rol creado (ID: {rol_id})\n")
    else:
        rol_id = rol_row[0]
        print(f"✓ Rol 'Administrador' encontrado (ID: {rol_id})\n")
    
    # Insertar Persona
    print("2️⃣  Creando registro de persona...")
    result = session.execute(text("""
        INSERT INTO persona (
            tipo_identificacion, numero_identificacion,
            primer_nombre, primer_apellido, fecha_nacimiento, type
        )
        VALUES ('CC', '1000000000', 'Admin', 'Sistema', NOW(), 'administrador')
        RETURNING id_persona
    """))
    persona_id = result.scalar()
    session.commit()
    print(f"   ✅ Persona creada (ID: {persona_id})\n")
    
    # Insertar Usuario
    print("3️⃣  Creando usuario...")
    session.execute(text("""
        INSERT INTO usuario (
            id_usuario, correo_electronico, contrasena,
            id_rol, activo, fecha_creacion
        )
        VALUES (:id, 'admin@colegio.edu', 'admin123', :rol_id, true, NOW())
    """), {"id": persona_id, "rol_id": rol_id})
    session.commit()
    print(f"   ✅ Usuario creado\n")
    
    # Insertar Administrador
    print("4️⃣  Asignando rol de administrador...")
    session.execute(text("""
        INSERT INTO administrador (id_administrador)
        VALUES (:id)
    """), {"id": persona_id})
    session.commit()
    print(f"   ✅ Administrador creado (ID: {persona_id})\n")
    
    print("="*60)
    print("✅ CREDENCIALES DE ACCESO:")
    print("-"*60)
    print(f"   📧 Email:      admin@colegio.edu")
    print(f"   🔑 Contraseña: admin123")
    print(f"   🆔 ID:         {persona_id}")
    print("-"*60)
    print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
    print("⚠️  La contraseña NO está hasheada (solo para desarrollo)\n")
    
    session.close()

except Exception as e:
    print(f"\n❌ Error: {e}\n")
    import traceback
    traceback.print_exc()
    if 'session' in locals():
        session.rollback()