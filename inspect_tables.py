from sqlalchemy import text, inspect
from app.infraestructura.db import engine

print("\n" + "="*60)
print("🔍 ESTRUCTURA DE TABLAS")
print("="*60 + "\n")

inspector = inspect(engine)

# Tablas importantes a revisar
tables_to_check = ['persona', 'usuario', 'rol', 'administrador']

for table_name in tables_to_check:
    print(f"\n📋 Tabla: {table_name}")
    print("-"*60)
    
    columns = inspector.get_columns(table_name)
    
    for col in columns:
        col_name = col['name']
        col_type = col['type']
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        primary = "🔑 PK" if col.get('primary_key') else ""
        
        print(f"   {col_name:30} {str(col_type):20} {nullable:10} {primary}")
    
    print("-"*60)

print("\n" + "="*60 + "\n")