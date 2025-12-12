"""
TEST INTERACTIVO: CU-25 Visualizar/Editar Hoja de Vida del Estudiante

Este script prueba la implementación del caso de uso CU-25.

ESCENARIOS DE PRUEBA:
1. Visualización de hoja de vida (modo interrumpible - PASO 5)
2. Edición válida de campos permitidos (PASO 6-14)
3. Validación de campos no permitidos (PASO 10.2)
4. Validación de formato JSON (PASO 10.1)
5. Validación de longitud máxima (PASO 10.3)
6. Cancelar edición sin guardar

PREREQUISITOS:
- Base de datos con estudiante id=2 (o modificar ID en el código)
- Estudiante debe tener hoja de vida creada (CU-19)
- Usuario id=1 debe existir
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from app.ui.components.dialogo_hoja_vida_visualizar import DialogoHojaVidaVisualizar
from app.services.servicio_hoja_vida import ServicioHojaVida


class TestCU25:
    """Test interactivo para CU-25"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TEST CU-25: Visualizar/Editar Hoja de Vida")
        self.root.geometry("650x550")
        
        # IDs de prueba
        self.estudiante_id = 2  # Santiago Díaz Martínez
        self.usuario_id = 1  # Director de grupo
        
        self._crear_interfaz()
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def _crear_interfaz(self):
        """Crear interfaz del test"""
        # Título
        frame_titulo = tk.Frame(self.root, bg="#9343FF", pady=15)
        frame_titulo.pack(fill=tk.X)
        
        tk.Label(
            frame_titulo,
            text="🧪 TEST INTERACTIVO: CU-25",
            font=("Arial", 16, "bold"),
            bg="#9343FF",
            fg="white"
        ).pack()
        
        tk.Label(
            frame_titulo,
            text="Visualizar/Editar Hoja de Vida del Estudiante",
            font=("Arial", 12),
            bg="#9343FF",
            fg="white"
        ).pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(config_frame, text="Estudiante ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_estudiante = ttk.Entry(config_frame, width=20)
        self.entry_estudiante.insert(0, str(self.estudiante_id))
        self.entry_estudiante.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        tk.Label(config_frame, text="Usuario ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_usuario = ttk.Entry(config_frame, width=20)
        self.entry_usuario.insert(0, str(self.usuario_id))
        self.entry_usuario.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Escenarios de prueba
        tests_frame = ttk.LabelFrame(main_frame, text="Escenarios de Prueba", padding=10)
        tests_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tests = [
            ("1️⃣ Visualizar Hoja de Vida", self._test_visualizacion,
             "PASO 5: Modo interrumpible, sin modificaciones"),
            
            ("2️⃣ Editar Campos Permitidos", self._test_editar_valido,
             "PASO 6-14: Editar y guardar correctamente"),
            
            ("3️⃣ Validar Formato JSON", self._test_validacion_json,
             "PASO 10.1: Detección de JSON inválido"),
            
            ("4️⃣ Validar Longitud Máxima", self._test_validacion_longitud,
             "PASO 10.3: Estado de salud >100 caracteres"),
            
            ("5️⃣ Cancelar Edición", self._test_cancelar_edicion,
             "Cancelar cambios sin guardar"),
            
            ("6️⃣ Ver Datos Cargados", self._test_ver_datos,
             "Verificar carga de datos (PASO 3)")
        ]
        
        for i, (texto, comando, descripcion) in enumerate(tests):
            frame = tk.Frame(tests_frame, relief=tk.GROOVE, borderwidth=1, pady=5, padx=5)
            frame.pack(fill=tk.X, pady=3)
            
            tk.Label(
                frame,
                text=texto,
                font=("Arial", 10, "bold"),
                anchor=tk.W
            ).pack(side=tk.LEFT, padx=(5, 10))
            
            ttk.Button(
                frame,
                text="▶ Ejecutar",
                command=comando
            ).pack(side=tk.RIGHT, padx=5)
            
            tk.Label(
                frame,
                text=descripcion,
                font=("Arial", 8),
                fg="gray",
                anchor=tk.W
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botón cerrar
        ttk.Button(
            main_frame,
            text="Cerrar Test",
            command=self.root.destroy
        ).pack(pady=(10, 0))
    
    def _obtener_ids(self):
        """Obtener IDs de los campos de entrada"""
        try:
            estudiante_id = int(self.entry_estudiante.get())
            usuario_id = int(self.entry_usuario.get())
            return estudiante_id, usuario_id
        except ValueError:
            messagebox.showerror("Error", "Los IDs deben ser números enteros")
            return None, None
    
    def _test_visualizacion(self):
        """TEST 1: Visualización de hoja de vida (modo interrumpible)"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        try:
            dialogo = DialogoHojaVidaVisualizar(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
            
            messagebox.showinfo(
                "Test Completado",
                "✅ TEST 1: Visualización\n\n"
                "Verificaciones:\n"
                "• Se desplegó la hoja de vida completa\n"
                "• Todos los campos están deshabilitados\n"
                "• Puedes cerrar sin afectar datos\n"
                "• Modo interrumpible activo"
            )
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_editar_valido(self):
        """TEST 2: Edición válida de campos permitidos"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        messagebox.showinfo(
            "TEST 2: Editar Campos Permitidos",
            "Instrucciones:\n\n"
            "1. Click en '✏️ Editar Hoja de Vida'\n"
            "2. Modificar cualquiera de los campos permitidos:\n"
            "   • Estado de salud\n"
            "   • Alergias (JSON)\n"
            "   • Tratamientos (JSON)\n"
            "   • Necesidades educativas (JSON)\n"
            "3. Click en '💾 Guardar Modificaciones'\n"
            "4. Verificar mensaje de éxito\n\n"
            "Este test valida el flujo PASO 6-14"
        )
        
        try:
            dialogo = DialogoHojaVidaVisualizar(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_validacion_json(self):
        """TEST 3: Validación de formato JSON"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        messagebox.showinfo(
            "TEST 3: Validar Formato JSON",
            "Instrucciones:\n\n"
            "1. Click en '✏️ Editar Hoja de Vida'\n"
            "2. En Alergias, escribir texto NO-JSON:\n"
            "   Ej: esto no es json válido\n"
            "3. Click en '💾 Guardar Modificaciones'\n"
            "4. DEBE aparecer error de formato JSON\n\n"
            "Esto valida PASO 10.1"
        )
        
        try:
            dialogo = DialogoHojaVidaVisualizar(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_validacion_longitud(self):
        """TEST 4: Validación de longitud máxima"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        texto_largo = "A" * 150  # Más de 100 caracteres
        
        messagebox.showinfo(
            "TEST 4: Validar Longitud Máxima",
            "Instrucciones:\n\n"
            "1. Click en '✏️ Editar Hoja de Vida'\n"
            "2. En Estado de salud, escribir más de 100 caracteres\n"
            f"   Puedes copiar esto: {texto_largo[:30]}...\n"
            "3. Observar contador en ROJO\n"
            "4. Click en '💾 Guardar' → ERROR\n\n"
            "Esto valida PASO 10.3"
        )
        
        try:
            dialogo = DialogoHojaVidaVisualizar(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_cancelar_edicion(self):
        """TEST 5: Cancelar edición sin guardar"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        messagebox.showinfo(
            "TEST 5: Cancelar Edición",
            "Instrucciones:\n\n"
            "1. Click en '✏️ Editar Hoja de Vida'\n"
            "2. Modificar CUALQUIER campo\n"
            "3. Click en '❌ Cancelar Edición'\n"
            "4. Confirmar que deseas cancelar\n"
            "5. Verificar que los campos vuelven a valores originales\n"
            "6. Verificar que vuelve a modo visualización"
        )
        
        try:
            dialogo = DialogoHojaVidaVisualizar(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_ver_datos(self):
        """TEST 6: Ver datos cargados de la hoja de vida"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        try:
            # PASO 3: Cargar datos
            datos = ServicioHojaVida.cargar_hoja_vida_estudiante(estudiante_id)
            
            # Mostrar información
            estudiante = datos['estudiante']
            hoja_vida = datos['hoja_vida']
            
            mensaje = (
                f"✅ DATOS CARGADOS CORRECTAMENTE\n\n"
                f"ESTUDIANTE:\n"
                f"• Código: {estudiante['codigo']}\n"
                f"• Nombre: {estudiante['primer_nombre']} {estudiante['primer_apellido']}\n"
                f"• Identificación: {estudiante['tipo_identificacion']} {estudiante['numero_identificacion']}\n\n"
                f"HOJA DE VIDA:\n"
                f"• ID: {hoja_vida['id']}\n"
                f"• Estado de salud: {hoja_vida['estado_salud'][:50] if hoja_vida['estado_salud'] else 'N/A'}...\n"
                f"• Alergias: {'Sí' if hoja_vida['alergias'] else 'No'}\n"
                f"• Tratamientos: {'Sí' if hoja_vida['tratamientos'] else 'No'}\n"
                f"• Necesidades educativas: {'Sí' if hoja_vida['necesidades_educativas'] else 'No'}\n"
                f"• Fecha creación: {hoja_vida['fecha_creacion']}\n"
            )
            
            messagebox.showinfo("Datos de Hoja de Vida", mensaje)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error al cargar datos:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")
    
    def run(self):
        """Ejecutar test"""
        self.root.mainloop()


def main():
    """Función principal"""
    print("=" * 70)
    print("TEST INTERACTIVO: CU-25 Visualizar/Editar Hoja de Vida del Estudiante")
    print("=" * 70)
    print()
    print("Este test permite verificar todos los aspectos del CU-25:")
    print("• Visualización interrumpible (PASO 5)")
    print("• Modo edición con campos permitidos (PASO 6-8)")
    print("• Validaciones completas (PASO 10)")
    print("• Manejo de errores (PASO 11)")
    print("• Guardado exitoso (PASO 12-14)")
    print()
    print("IMPORTANTE:")
    print("• Asegúrate de que el estudiante ID=2 existe")
    print("• El estudiante debe tener una hoja de vida creada (CU-19)")
    print("• Puedes modificar los IDs en la interfaz")
    print()
    print("-" * 70)
    
    test = TestCU25()
    test.run()


if __name__ == "__main__":
    main()
