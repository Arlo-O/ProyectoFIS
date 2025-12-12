"""
Script para agregar el campo justificacion_rechazo a la tabla aspirante
CU-18: Admitir aspirante
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy import text
from app.data.db import SessionLocal

def agregar_campo_justificacion_rechazo():
    """Agrega el campo justificacion_rechazo a la tabla aspirante"""
    session = SessionLocal()
    
    try:
        # Verificar si la columna ya existe
        query_verificar = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='aspirante' 
            AND column_name='justificacion_rechazo'
        """)
        
        resultado = session.execute(query_verificar).fetchone()
        
        if resultado:
            print("✓ El campo 'justificacion_rechazo' ya existe en la tabla 'aspirante'")
            return True, "Campo ya existe"
        
        # Agregar la columna
        query_agregar = text("""
            ALTER TABLE aspirante 
            ADD COLUMN justificacion_rechazo TEXT
        """)
        
        session.execute(query_agregar)
        session.commit()
        
        print("✓ Campo 'justificacion_rechazo' agregado exitosamente a la tabla 'aspirante'")
        return True, "Campo agregado exitosamente"
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error al agregar campo: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)
    
    finally:
        session.close()

if __name__ == "__main__":
    print("=" * 60)
    print("ACTUALIZACIÓN DE BASE DE DATOS - CU-18: Admitir aspirante")
    print("=" * 60)
    print()
    
    exito, mensaje = agregar_campo_justificacion_rechazo()
    
    print()
    print("=" * 60)
    if exito:
        print("✓ Actualización completada exitosamente")
    else:
        print("✗ Error en la actualización")
    print("=" * 60)
