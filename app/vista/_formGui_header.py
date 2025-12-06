"""
Archivo: formGui.py
Formulario de preinscripción de 4 pasos para aspirantes al colegio.

Este módulo implementa el proceso completo de preinscripción en línea,
dividido en 4 pasos secuenciales para facilitar el ingreso de información.

Pasos del formulario:
1. Datos del Estudiante - Información básica del niño/aspirante
2. Datos de los Acudientes - Información de padres/responsables  
3. Información Médica y de Emergencia - Alergias, medicamentos, contactos
4. Confirmación y Términos - Resumen y aceptación de términos

Características técnicas:
- Scroll vertical automático para formularios largos
- Navegación entre pasos (Anterior/Siguiente)
- Diálogo de confirmación al enviar
- Barra de progreso visual (1/4, 2/4, etc.)
- Funciones create_step1() a create_step4() retornan frames completos

IMPORTANTE: Actualmente el envío es simulado (solo UI).
Para conectar con backend real, integrar servicios en el callback de envío.
"""

