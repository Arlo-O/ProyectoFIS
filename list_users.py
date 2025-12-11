from sqlalchemy import text
from app.infraestructura.db import engine

print("\n" + "="*60)
print("👥 USUARIOS REGISTRADOS EN EL SISTEMA")
print("="*60 + "\n")

try:
    with engine.connect() as conn:
        # Listar todos los usuarios con sus datos
        result = conn.execute(text("""
            SELECT 
                p.id_persona,
                p.type,
                p.tipo_identificacion,
                p.numero_identificacion,
                p.primer_nombre,
                p.segundo_nombre,
                p.primer_apellido,
                p.segundo_apellido,
                u.correo_electronico,
                u.activo,
                r.nombre_rol
            FROM persona p
            LEFT JOIN usuario u ON p.id_persona = u.id_usuario
            LEFT JOIN rol r ON u.id_rol = r.id_rol
            ORDER BY p.id_persona
        """))
        
        usuarios = result.fetchall()
        
        if not usuarios:
            print("⚠️  No hay usuarios en el sistema\n")
        else:
            print(f"Total de registros: {len(usuarios)}\n")
            print("-"*60)
            
            for user in usuarios:
                id_persona = user[0]
                tipo = user[1]
                tipo_id = user[2]
                num_id = user[3]
                nombre = f"{user[4] or ''} {user[5] or ''}".strip()
                apellido = f"{user[6] or ''} {user[7] or ''}".strip()
                email = user[8] or "Sin email"
                activo = "✅" if user[9] else "❌"
                rol = user[10] or "Sin rol"
                
                print(f"\n🆔 ID: {id_persona}")
                print(f"   👤 Nombre:    {nombre} {apellido}")
                print(f"   🎭 Tipo:      {tipo}")
                print(f"   📧 Email:     {email}")
                print(f"   🎫 Rol:       {rol}")
                print(f"   📄 Doc:       {tipo_id} {num_id}")
                print(f"   📊 Estado:    {activo} {'Activo' if user[9] else 'Inactivo'}")
            
            print("\n" + "-"*60)
        
        # Ver distribución por tipo
        print("\n📊 CONTEO POR TIPO DE USUARIO:")
        print("-"*60)
        
        for tipo in ['estudiante', 'profesor', 'acudiente', 'aspirante', 'directivo', 'administrador']:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {tipo}"))
            count = result.scalar()
            if count > 0:
                print(f"   • {tipo.capitalize():20} : {count}")
        
        print("-"*60 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}\n")
    import traceback
    traceback.print_exc()