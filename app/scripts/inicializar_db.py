"""
Script para inicializar la base de datos con datos de prueba
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import init_db, SessionLocal
from servicios.servicio_autenticacion import ServicioAutenticacion


def crear_datos_prueba():
    """Crea datos de prueba para la aplicación"""
    from modelos.rol import Rol
    from modelos.usuario import Usuario
    from repositorios.repositorio_rol import RepositorioRol
    from repositorios.repositorio_usuario import RepositorioUsuario
    
    # Inicializar base de datos
    print("Inicializando base de datos...")
    init_db()
    
    db = SessionLocal()
    servicio_auth = ServicioAutenticacion()
    repo_rol = RepositorioRol(db)
    repo_usuario = RepositorioUsuario(db)
    
    try:
        # Crear roles
        print("Creando roles...")
        rol_admin = Rol(1, 'Administrador', 'Administrador del sistema')
        rol_directivo = Rol(2, 'Directivo', 'Director/Directora del colegio')
        rol_profesor = Rol(3, 'Profesor', 'Docente')
        rol_acudiente = Rol(4, 'Acudiente', 'Padre/Madre/Acudiente')
        
        repo_rol.crear(rol_admin)
        repo_rol.crear(rol_directivo)
        repo_rol.crear(rol_profesor)
        repo_rol.crear(rol_acudiente)
        
        # Crear usuarios de prueba
        print("Creando usuarios de prueba...")
        
        contraseña_admin = servicio_auth.cifrar_contrasena('admin123')
        usuario_admin = Usuario(
            idUsuario=1,
            username='admin',
            correoElectronico='admin@colegio.edu',
            rol=rol_admin,
            contrasena=contraseña_admin
        )
        repo_usuario.crear(usuario_admin)
        
        contraseña_directivo = servicio_auth.cifrar_contrasena('directivo123')
        usuario_directivo = Usuario(
            idUsuario=2,
            username='directivo',
            correoElectronico='directivo@colegio.edu',
            rol=rol_directivo,
            contrasena=contraseña_directivo
        )
        repo_usuario.crear(usuario_directivo)
        
        contraseña_profesor = servicio_auth.cifrar_contrasena('profesor123')
        usuario_profesor = Usuario(
            idUsuario=3,
            username='profesor',
            correoElectronico='profesor@colegio.edu',
            rol=rol_profesor,
            contrasena=contraseña_profesor
        )
        repo_usuario.crear(usuario_profesor)
        
        contraseña_acudiente = servicio_auth.cifrar_contrasena('acudiente123')
        usuario_acudiente = Usuario(
            idUsuario=4,
            username='acudiente',
            correoElectronico='acudiente@colegio.edu',
            rol=rol_acudiente,
            contrasena=contraseña_acudiente
        )
        repo_usuario.crear(usuario_acudiente)
        
        print("✓ Base de datos inicializada correctamente")
        print("\nUsuarios de prueba creados:")
        print("  - admin / admin123")
        print("  - directivo / directivo123")
        print("  - profesor / profesor123")
        print("  - acudiente / acudiente123")
        
    except Exception as e:
        print(f"Error al crear datos de prueba: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    crear_datos_prueba()
