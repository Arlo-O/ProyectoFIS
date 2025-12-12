-- ============================================================
-- ACTUALIZACIÓN BD PARA CU-19: Crear hoja de vida del estudiante
-- ============================================================
-- Este script agrega campos adicionales a la tabla hoja_vida
-- Ejecutar con el usuario dueño de la base de datos (postgres)

-- Verificar y agregar columnas faltantes
DO $$ 
BEGIN
    -- Agregar promedio_general si no existe
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name='hoja_vida' 
        AND column_name='promedio_general'
    ) THEN
        ALTER TABLE hoja_vida ADD COLUMN promedio_general REAL DEFAULT 0.0;
        RAISE NOTICE 'Columna promedio_general agregada exitosamente';
    ELSE
        RAISE NOTICE 'La columna promedio_general ya existe';
    END IF;
    
    -- Agregar fecha_creacion si no existe
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name='hoja_vida' 
        AND column_name='fecha_creacion'
    ) THEN
        ALTER TABLE hoja_vida ADD COLUMN fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        RAISE NOTICE 'Columna fecha_creacion agregada exitosamente';
    ELSE
        RAISE NOTICE 'La columna fecha_creacion ya existe';
    END IF;
    
    -- Agregar usuario_creador si no existe
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name='hoja_vida' 
        AND column_name='usuario_creador'
    ) THEN
        ALTER TABLE hoja_vida ADD COLUMN usuario_creador INTEGER REFERENCES usuario(id_usuario);
        RAISE NOTICE 'Columna usuario_creador agregada exitosamente';
    ELSE
        RAISE NOTICE 'La columna usuario_creador ya existe';
    END IF;
END $$;

-- Verificar estructura final
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'hoja_vida'
ORDER BY ordinal_position;
