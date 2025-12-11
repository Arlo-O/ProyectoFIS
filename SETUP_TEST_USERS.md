# Guía: Opción 1 - Variables de Entorno (.env) para Datos de Prueba

## Resumen

Con la **Opción 1**, las credenciales de prueba se cargan desde el archivo `.env`:
- ✅ **No hay datos hardcodeados en el código**
- ✅ **Puedes seguir registrando usuarios nuevos en la BD**
- ✅ **Los usuarios de prueba aparecen en la UI solo en desarrollo**
- ✅ **En producción, solo comentas las líneas de .env**

---

## Flujo

```
┌──────────────────────────────────────────────────────────────────┐
│ USUARIO INTENTA LOGIN                                            │
└──────────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 1. Ingresa email/contraseña en UI                                │
│    (puede usar usuario de prueba de .env O usuario registrado)  │
└──────────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 2. AuthenticationService.authenticate() → BD                     │
│    (NO lee .env, siempre consulta BD)                           │
└──────────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────────┐
│ 3. BD retorna Usuario o None                                    │
│    - Si existe → Login exitoso                                  │
│    - Si NO existe → "Credenciales incorrectas"                 │
│    - .env solo sirve como REFERENCIA de qué probar             │
└──────────────────────────────────────────────────────────────────┘
```

---

## Instalación

### Paso 1: Archivo `.env` ya está configurado
El archivo `.env` incluye:
```bash
TEST_ADMIN_EMAIL=admin@colegio.edu
TEST_ADMIN_PASSWORD=admin123
TEST_DIRECTOR_EMAIL=director@colegio.edu
TEST_DIRECTOR_PASSWORD=dir123
TEST_TEACHER_EMAIL=profesor@colegio.edu
TEST_TEACHER_PASSWORD=prof123
TEST_PARENT_EMAIL=padre@colegio.edu
TEST_PARENT_PASSWORD=papa123
```

### Paso 2: Insertar usuarios de prueba en BD (una sola vez)
```bash
python scripts/insert_test_users.py
```

**Salida esperada:**
```
======================================================================
Insertando usuarios de prueba en la BD...
======================================================================

[*] Verificando/creando roles...
    ✓ Rol 'administrador' OK
    ✓ Rol 'director' OK
    ✓ Rol 'profesor' OK
    ✓ Rol 'acudiente' OK

[*] Verificando/creando usuarios de prueba...
    ✓ Usuario admin@colegio.edu creado correctamente
    ✓ Usuario director@colegio.edu creado correctamente
    ✓ Usuario profesor@colegio.edu creado correctamente
    ✓ Usuario padre@colegio.edu creado correctamente

======================================================================
✓ Usuarios de prueba insertados correctamente
======================================================================

[*] Credenciales de prueba (desde .env):

    Email: admin@colegio.edu
    Contraseña: admin123
    Rol: administrador

    Email: director@colegio.edu
    Contraseña: dir123
    Rol: director

    Email: profesor@colegio.edu
    Contraseña: prof123
    Rol: profesor

    Email: padre@colegio.edu
    Contraseña: papa123
    Rol: acudiente
```

### Paso 3: Ejecutar la aplicación
```bash
python run_app.py
```

En la UI de login verás:
```
Usuarios de prueba:
• admin@colegio.edu / admin123 (Administrador)
• director@colegio.edu / dir123 (Director)
• profesor@colegio.edu / prof123 (Profesor)
• padre@colegio.edu / papa123 (Acudiente)
```

---

## ¿Cómo Registrar Nuevos Usuarios?

### Opción A: Directamente en BD (SQL)
```sql
-- Supongamos que ya existe el rol "administrador"
INSERT INTO usuario (id_usuario, correo_electronico, contrasena, id_rol, activo, fecha_creacion)
VALUES (
    (SELECT MAX(id_persona) FROM persona),  -- Asumir que existe persona
    'juan@colegio.edu',
    'micontraseña123',
    (SELECT id_rol FROM rol WHERE nombre_rol = 'administrador'),
    true,
    NOW()
);
```

### Opción B: Script Python
```python
from app.infraestructura.uow import uow
from app.modelos.usuarios.usuario import Usuario
from app.modelos.usuarios.persona import Persona
from datetime import datetime

with uow() as unit_of_work:
    persona = Persona(
        numero_identificacion="1234567890",
        tipo_identificacion="CC",
        primer_nombre="Juan",
        primer_apellido="Pérez",
        fecha_nacimiento=datetime(1995, 5, 15),
        type="Usuario"
    )
    
    usuario = Usuario(
        correo_electronico="juan@colegio.edu",
        contrasena="micontraseña123",  # Usar bcrypt en producción
        id_rol=1,  # ID del rol
        activo=True,
        fecha_creacion=datetime.now()
    )
    usuario.persona = persona
    
    unit_of_work.usuarios.add(usuario)
    unit_of_work.commit()
    print("✓ Usuario juan@colegio.edu registrado")
```

### Opción C: Formulario de Pre-inscripción (cuando esté implementado)
La UI ya tiene un módulo de pre-inscripción que permite registrar estudiantes nuevos.

---

## Flujos de Prueba

### ✅ Escenario 1: Login con usuario de prueba
```
1. Inicia app: ves usuarios de prueba en la UI
2. Ingresa: admin@colegio.edu / admin123
3. Resultado: ✓ Login exitoso → Dashboard de Admin
```

### ✅ Escenario 2: Login con usuario registrado personalmente
```
1. Registras: juan@colegio.edu / mipass123 en BD (vía SQL o script)
2. Inicia app
3. Ingresa: juan@colegio.edu / mipass123
4. Resultado: ✓ Login exitoso → Dashboard según su rol
```

### ✅ Escenario 3: Login fallido (usuario no existe)
```
1. Ingresa: fake@colegio.edu / anypassword
2. Resultado: ✗ "Credenciales incorrectas"
   (No importa si está en .env, si no existe en BD, falla)
```

### ✅ Escenario 4: Login fallido (contraseña incorrecta)
```
1. Ingresa: admin@colegio.edu / wrongpassword
2. Resultado: ✗ "Credenciales incorrectas"
   (Usuario existe, pero contraseña no coincide)
```

---

## Cambio a Producción

### 1. Cambiar ENVIRONMENT en `.env`:
```bash
ENVIRONMENT=production
```

### 2. Resultado:
- ❌ Los usuarios de prueba **NO aparecen** en la UI
- ✅ Solo se pueden loguear usuarios **reales** de BD
- ✅ Sigue siendo seguro: autenticación contra BD

### 3. Proteger credenciales:
```bash
# En producción, comentar o eliminar:
# TEST_ADMIN_EMAIL=...
# TEST_ADMIN_PASSWORD=...
# etc.
```

---

## Seguridad

### ⚠️ Actual (DESARROLLO):
```python
usuario.contrasena = password  # Texto plano ❌
```

### ✅ Para Producción:
```python
import bcrypt

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
usuario.contrasena = hashed.decode()

# En login:
if bcrypt.checkpw(password.encode(), usuario.contrasena.encode()):
    # Login exitoso
```

---

## Resumen

| Aspecto | Opción 1 (.env) |
|---|---|
| ¿Datos hardcodeados en código? | ❌ No (en `.env`) |
| ¿Puedo registrar nuevos usuarios? | ✅ Sí (en BD) |
| ¿Autentica contra BD? | ✅ Sí (siempre) |
| ¿Fácil para desarrollo? | ✅ Sí |
| ¿Fácil para producción? | ✅ Sí (cambiar ENVIRONMENT) |
| ¿Requiere fixture/docker? | ❌ No |

---

## Archivos Involucrados

- **`.env`** — Variables de entorno con credenciales de prueba
- **`scripts/insert_test_users.py`** — Script para poblar BD con usuarios de prueba
- **`app/vista/app_gui.py`** — Lee `.env` y muestra usuarios de prueba solo si `ENVIRONMENT=development`
- **`app/vista/auth_service.py`** — Autentica SIEMPRE contra BD (ignora `.env`)

---

**¡Listo!** Ahora tienes datos de prueba en `.env` sin hardcodear nada en el código, y puedes registrar todos los usuarios que necesites en la BD. 🚀
