#!/usr/bin/env python3
"""
Script para convertir atributos privados (__atributo) a públicos (atributo)
en todos los modelos para compatibilidad con SQLAlchemy.

Uso:
    python fix_private_attrs.py
"""

import os
import re
from pathlib import Path

def fix_file(filepath: Path) -> tuple[bool, int]:
    """
    Reemplaza self.__atributo por self.atributo en un archivo.
    
    Returns:
        (cambios_realizados, num_reemplazos)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Patrón para capturar self.__atributo (con word boundary)
        # Captura: self.__nombre_atributo
        pattern = r'\bself\.__(\w+)\b'
        
        # Reemplazar por self.atributo
        new_content = re.sub(pattern, r'self.\1', content)
        
        # Contar reemplazos
        num_replacements = len(re.findall(pattern, original_content))
        
        if new_content != original_content:
            # Hacer backup
            backup_path = filepath.with_suffix('.py.bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Guardar archivo modificado
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, num_replacements
        
        return False, 0
        
    except Exception as e:
        print(f"❌ Error procesando {filepath}: {e}")
        return False, 0


def main():
    """Procesa todos los archivos Python en app/modelos/"""
    
    modelos_dir = Path("app/modelos")
    
    if not modelos_dir.exists():
        print(f"❌ No se encuentra el directorio: {modelos_dir}")
        print("   Ejecuta este script desde la raíz del proyecto")
        return
    
    print("🔍 Buscando archivos con atributos privados...\n")
    
    files_modified = 0
    total_replacements = 0
    files_list = []
    
    # Buscar todos los archivos .py recursivamente
    for py_file in modelos_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        modified, count = fix_file(py_file)
        
        if modified:
            files_modified += 1
            total_replacements += count
            files_list.append((py_file, count))
            print(f"✅ {py_file.relative_to('app/modelos')}: {count} reemplazos")
    
    print("\n" + "="*60)
    print(f"📊 RESUMEN:")
    print(f"   Archivos modificados: {files_modified}")
    print(f"   Total de reemplazos: {total_replacements}")
    print("="*60)
    
    if files_modified > 0:
        print("\n⚠️  IMPORTANTE:")
        print("   1. Se crearon archivos .bak como backup")
        print("   2. Revisa los cambios antes de hacer commit")
        print("   3. Prueba que todo funcione correctamente")
        print("   4. Si hay problemas, restaura desde los .bak")
        print("\n📝 Archivos modificados:")
        for file, count in files_list:
            print(f"   - {file.relative_to('app/modelos')}")
    else:
        print("\n✅ No se encontraron archivos para modificar")


if __name__ == "__main__":
    main()