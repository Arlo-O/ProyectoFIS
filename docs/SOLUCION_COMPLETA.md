# 🔧 GUÍA DE SOLUCIÓN COMPLETA

## ✅ Problemas Corregidos

### 1. Error: "no existe la columna permiso.fecha_creacion"
**Causa:** Las tablas `rol` y `permiso` no tienen columnas de fecha, pero las clases Python sí las usaban.

**Solución:**
- ✅ Actualizado `app/core/usuarios/rol.py` - Eliminados parámetros `fecha_creacion` y `fecha_actualizacion`
- ✅ Actualizado `app/core/usuarios/permiso.py` - Eliminados parámetros `fecha_creacion` y `fecha_actualizacion`
- ✅ Actualizado `seed_permisos.py` - INSERT sin columnas de fecha
- ✅ Actualizado `app/data/mappers.py` - tabla `permiso` solo tiene 3 columnas

### 2. Error: "Dashboard retorna None"
**Causa:** Los decoradores `@require_permission` retornaban `None` cuando no había permisos.

**Solución:**
- ✅ Actualizado `app/ui/main.py` - Mejor manejo de errores en `login_to_dashboard()`
- ✅ Validación de None antes de usar dashboard_frame
- ✅ Mejor búsqueda del main_frame
- ✅ Manejo seguro de atributos de usuario

### 3. Error: "Lista de permisos vacía"
**Causa:** Los permisos no estaban cargados en la base de datos.

**Solución:**
- ✅ Ejecutar `seed_permisos.py` después de crear usuarios
- ✅ Script de reinicio automático incluido

---

## 📋 PROCESO DE REINICIO COMPLETO

Sigue estos pasos **EN ORDEN** para reiniciar completamente la base de datos:

### Paso 1: Ejecutar SQL en pgAdmin
1. Abre pgAdmin
2. Conecta a la BD `fis_db_desarrollo`
3. Abre el archivo `scripts/clean_database.sql`
4. Ejecuta el script completo
5. Verifica que no haya errores

**Este script:**
- Elimina todos los datos
- Elimina todas las tablas
- Reinicia secuencias
- Recrea todas las tablas con la arquitectura correcta
- Inserta 5 roles base (administrador, director, profesor, acudiente, aspirante)

### Paso 2: Ejecutar Script Python de Reinicio
```bash
python scripts/reiniciar_bd_completa.py
```

Este script:
1. Te pide confirmar que ejecutaste el SQL (Paso 1)
2. Ejecuta `scripts/create_test_users.py` - Crea 4 usuarios de prueba con passwords hasheados
3. Ejecuta `seed_permisos.py` - Crea permisos y los asigna a roles

---

## 👥 USUARIOS DE PRUEBA CREADOS

| Usuario    | Correo                    | Contraseña   | Rol           |
|-----------|---------------------------|--------------|---------------|
| admin     | admin@fis.edu.co          | admin123     | Administrador |
| director  | director@fis.edu.co       | director123  | Director      |
| profesor  | profesor@fis.edu.co       | profesor123  | Profesor      |
| padre     | padre@fis.edu.co          | padre123     | Acudiente     |

---

## 🔐 PERMISOS POR ROL

### Administrador (admin)
- ✅ acceder_admin
- ✅ gestionar_usuarios
- ✅ gestionar_roles
- ✅ gestionar_permisos
- ✅ ver_reportes
- ✅ generar_reportes
- ✅ ver_citaciones
- ✅ crear_citaciones

### Director
- ✅ acceder_director
- ✅ gestionar_grupos
- ✅ gestionar_profesores
- ✅ ver_estudiantes
- ✅ ver_reportes
- ✅ generar_reportes
- ✅ ver_citaciones
- ✅ crear_citaciones

### Profesor
- ✅ acceder_profesor
- ✅ ver_calificaciones
- ✅ registrar_calificaciones
- ✅ crear_anotaciones
- ✅ ver_asignaciones
- ✅ ver_estudiantes
- ✅ ver_citaciones

### Acudiente
- ✅ acceder_acudiente
- ✅ ver_desempenio
- ✅ ver_comunicaciones

---

## 🚀 EJECUTAR LA APLICACIÓN

Después de completar el reinicio:

```bash
python run_app.py
```

**Loguéate con:**
- Correo: `admin@fis.edu.co`
- Contraseña: `admin123`

**Deberías poder:**
- ✅ Iniciar sesión sin errores
- ✅ Ver el dashboard de administrador
- ✅ Sin errores de "columna no existe"
- ✅ Sin errores de "dashboard retorna None"
- ✅ Permisos cargados correctamente

---

## 🔍 VERIFICACIÓN DE PERMISOS (Opcional)

Para verificar que los permisos se cargaron correctamente, ejecuta en pgAdmin:

```sql
-- Ver todos los permisos
SELECT * FROM permiso;

-- Ver permisos del rol Administrador (ID = 1)
SELECT p.nombre, p.descripcion
FROM permiso p
JOIN rol_permiso rp ON p.id_permiso = rp.id_permiso
WHERE rp.id_rol = 1;

-- Ver relación usuario-rol
SELECT u.correo_electronico, r.nombre_rol
FROM usuario u
JOIN rol r ON u.id_rol = r.id_rol;
```

---

## ⚠️ NOTAS IMPORTANTES

1. **SIEMPRE ejecuta clean_database.sql ANTES del script Python**
   - Si ejecutas los scripts Python sin limpiar primero, tendrás errores de FK

2. **Las contraseñas están hasheadas con bcrypt**
   - No puedes usar contraseñas en texto plano
   - El script `create_test_users.py` ya hashea las contraseñas

3. **Arquitectura de herencia:**
   - **Administrador** hereda de Usuario (única herencia)
   - **Profesor, Directivo, Acudiente, Aspirante** heredan de Persona con FK a Usuario
   - **Estudiante** hereda de Persona SIN Usuario

4. **La relación Rol-Permiso es many-to-many:**
   - Tabla intermedia: `rol_permiso`
   - Correctamente configurada en `app/data/mappers.py`

---

## 📝 ARCHIVOS MODIFICADOS

1. ✅ `app/core/usuarios/rol.py` - Eliminados parámetros de fecha
2. ✅ `app/core/usuarios/permiso.py` - Eliminados parámetros de fecha
3. ✅ `app/data/mappers.py` - Tabla permiso sin columnas de fecha
4. ✅ `seed_permisos.py` - INSERT sin fechas
5. ✅ `app/ui/main.py` - Mejor manejo de errores en login
6. ✅ `scripts/clean_database.sql` - Ya estaba correcto
7. ✅ `scripts/create_test_users.py` - Ya estaba correcto
8. ✅ **NUEVO:** `scripts/reiniciar_bd_completa.py` - Script de reinicio automático

---

## 🎯 PRÓXIMOS PASOS

Después de ejecutar el reinicio y verificar que funciona:

1. ✅ Login funciona correctamente
2. ✅ Dashboard se muestra sin errores
3. ✅ Permisos cargados y funcionando
4. Continuar con desarrollo de funcionalidades adicionales

---

**¡Todo listo para trabajar sin errores!** 🎉
