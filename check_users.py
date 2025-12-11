from sqlalchemy import select, text
from app.infraestructura.db import SessionLocal, engine
from app.infraestructura.mappers import start_mappers

print("\n" + "="*60)
print("👥 VERIFICACIÓN DE USUARIOS EN LA BASE DE DATOS")
print("="*60 + "\n")

start_mappers()

try:
    session = SessionLocal()
    
    # Contar usuarios por tabla
    with engine.connect() as conn:
        # Personas
        result = conn.execute(text("SELECT COUNT(*) FROM persona"))
        personas = result.scalar()
        
        # Usuarios
        result = conn.execute(text("SELECT COUNT(*) FROM usuario"))
        usuarios = result.scalar()
        
        # Administradores
        result = conn.execute(text("SELECT COUNT(*) FROM administrador"))
        admins = result.scalar()
        
        # Roles
        result = conn.execute(text("SELECT COUNT(*) FROM rol"))
        roles = result.scalar()
    
    print(f"📊 Resumen:")
    print(f"   Personas:        {personas}")
    print(f"   Usuarios:        {usuarios}")
    print(f"   Administradores: {admins}")
    print(f"   Roles:           {roles}")
    print()
    
    if admins == 0:
        print("⚠️  No hay administradores en el sistema")
        print("\n💡 Siguiente paso: Crear usuario admin")
        print("   python seed_admin.py\n")
    else:
        print("✅ Ya existen administradores")
        
        # Listar admins
        result = session.execute(text("""
            SELECT u.correo_electronico, p.primer_nombre, p.primer_apellido
            FROM administrador a
            JOIN usuario u ON a.id_administrador = u.id_usuario
            JOIN persona p ON u.id_usuario = p.id_persona
        """))
        
        print("\n📋 Administradores registrados:")
        for row in result:
            print(f"   • {row[1]} {row[2]} ({row[0]})")
        print()
    
    session.close()

except Exception as e:
    print(f"\n❌ Error: {e}\n")
    import traceback
    traceback.print_exc()