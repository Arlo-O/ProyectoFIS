-- ============================================================
-- ACTUALIZACIÓN BD PARA CU-18: Admitir aspirante
-- ============================================================
-- Este script agrega el campo justificacion_rechazo a la tabla aspirante
-- Ejecutar con el usuario dueño de la base de datos (postgres)

-- Verificar si la columna ya existe
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name='aspirante' 
        AND column_name='justificacion_rechazo'
    ) THEN
        -- Agregar columna si no existe
        ALTER TABLE aspirante ADD COLUMN justificacion_rechazo TEXT;
        RAISE NOTICE 'Columna justificacion_rechazo agregada exitosamente';
    ELSE
        RAISE NOTICE 'La columna justificacion_rechazo ya existe';
    END IF;
END $$;
