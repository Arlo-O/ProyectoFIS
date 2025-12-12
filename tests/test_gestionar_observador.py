"""
TEST INTERACTIVO: CU-24 Gestionar Observador del Estudiante

Este script prueba la implementación del caso de uso CU-24.

ESCENARIOS DE PRUEBA:
1. Visualización del observador (modo interrumpible - PASO 5)
2. Modificación válida de comportamiento (PASO 6-14)
3. Agregado válido de anotación (PASO 6-14)
4. Validación de campos no permitidos (PASO 11)
5. Validación de campos vacíos (PASO 11.3)
6. Validación de longitud de campos (PASO 11.2)

PREREQUISITOS:
- Base de datos con estudiante id=2 (o modificar ID en el código)
- Estudiante debe tener observador asociado
- Usuario id=1 debe existir
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from app.ui.components.dialogo_observador import DialogoObservador
from app.services.servicio_observador import ServicioObservador


class TestCU24:
    """Test interactivo para CU-24"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TEST CU-24: Gestionar Observador del Estudiante")
        self.root.geometry("600x500")
        
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
        frame_titulo = tk.Frame(self.root, bg="#007bff", pady=15)
        frame_titulo.pack(fill=tk.X)
        
        tk.Label(
            frame_titulo,
            text="🧪 TEST INTERACTIVO: CU-24",
            font=("Arial", 16, "bold"),
            bg="#007bff",
            fg="white"
        ).pack()
        
        tk.Label(
            frame_titulo,
            text="Gestionar Observador del Estudiante",
            font=("Arial", 12),
            bg="#007bff",
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
            ("1️⃣ Abrir Observador (Visualización)", self._test_visualizacion,
             "PASO 5: Modo interrumpible, sin modificaciones"),
            
            ("2️⃣ Modificar Comportamiento", self._test_modificar_comportamiento,
             "PASO 6-14: Editar comportamiento general"),
            
            ("3️⃣ Agregar Anotación", self._test_agregar_anotacion,
             "PASO 6-14: Nueva observación"),
            
            ("4️⃣ Validar Campos Vacíos", self._test_validacion_vacios,
             "PASO 11.3: Detección de campos vacíos"),
            
            ("5️⃣ Validar Longitud Máxima", self._test_validacion_longitud,
             "PASO 11.2: Validación de límites"),
            
            ("6️⃣ Ver Datos del Observador", self._test_ver_datos,
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
        """TEST 1: Visualización del observador (modo interrumpible)"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        try:
            dialogo = DialogoObservador(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
            
            messagebox.showinfo(
                "Test Completado",
                "✅ TEST 1: Visualización\n\n"
                "Verificaciones:\n"
                "• Se desplegó la información del observador\n"
                "• Campos están deshabilitados (modo visualización)\n"
                "• Puedes cerrar sin afectar datos"
            )
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_modificar_comportamiento(self):
        """TEST 2: Modificar comportamiento (flujo completo)"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        messagebox.showinfo(
            "TEST 2: Modificar Comportamiento",
            "Instrucciones:\n\n"
            "1. Click en 'Modificar Comportamiento'\n"
            "2. Editar el texto del campo\n"
            "3. Click en 'Guardar Cambios'\n"
            "4. Verificar mensaje de éxito\n\n"
            "Este test valida el flujo PASO 6-14"
        )
        
        try:
            dialogo = DialogoObservador(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_agregar_anotacion(self):
        """TEST 3: Agregar nueva anotación"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        messagebox.showinfo(
            "TEST 3: Agregar Anotación",
            "Instrucciones:\n\n"
            "1. Click en 'Agregar Anotación'\n"
            "2. Ingresar categoría y detalle\n"
            "3. Click en 'Guardar Cambios'\n"
            "4. Verificar que aparece en el listado\n\n"
            "Este test valida observaciones (PASO 7)"
        )
        
        try:
            dialogo = DialogoObservador(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_validacion_vacios(self):
        """TEST 4: Validación de campos vacíos"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        messagebox.showinfo(
            "TEST 4: Validar Campos Vacíos",
            "Instrucciones:\n\n"
            "1. Click en 'Modificar Comportamiento'\n"
            "2. Borrar TODO el contenido\n"
            "3. Click en 'Guardar Cambios'\n"
            "4. DEBE aparecer error: 'no puede estar vacío'\n\n"
            "Esto valida PASO 11.3"
        )
        
        try:
            dialogo = DialogoObservador(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_validacion_longitud(self):
        """TEST 5: Validación de longitud máxima"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        messagebox.showinfo(
            "TEST 5: Validar Longitud Máxima",
            "Instrucciones:\n\n"
            "1. Click en 'Agregar Anotación'\n"
            "2. Ingresar texto MUY LARGO en:\n"
            "   - Categoría (>50 caracteres)\n"
            "   - Detalle (>200 caracteres)\n"
            "3. Observar contador en ROJO\n"
            "4. Click en 'Guardar' → ERROR\n\n"
            "Esto valida PASO 11.2"
        )
        
        try:
            dialogo = DialogoObservador(self.root, estudiante_id, usuario_id)
            self.root.wait_window(dialogo)
        except Exception as e:
            messagebox.showerror("Error en Test", f"Error: {str(e)}")
    
    def _test_ver_datos(self):
        """TEST 6: Ver datos cargados del observador"""
        estudiante_id, usuario_id = self._obtener_ids()
        if estudiante_id is None:
            return
        
        try:
            # PASO 3: Cargar datos
            datos = ServicioObservador.cargar_observador_estudiante(estudiante_id)
            
            # Mostrar información
            estudiante = datos['estudiante']
            observador = datos['observador']
            anotaciones = datos['anotaciones']
            
            mensaje = (
                f"✅ DATOS CARGADOS CORRECTAMENTE\n\n"
                f"ESTUDIANTE:\n"
                f"• Código: {estudiante['codigo']}\n"
                f"• Nombre: {estudiante['nombres']} {estudiante['apellidos']}\n\n"
                f"OBSERVADOR:\n"
                f"• ID: {observador['id']}\n"
                f"• Comportamiento: {observador['comportamiento_general'][:50]}...\n\n"
                f"ANOTACIONES:\n"
                f"• Total: {len(anotaciones)}\n"
            )
            
            if anotaciones:
                mensaje += f"• Última: {anotaciones[0]['categoria']} ({anotaciones[0]['fecha']})\n"
            
            messagebox.showinfo("Datos del Observador", mensaje)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error al cargar datos:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")
    
    def run(self):
        """Ejecutar test"""
        self.root.mainloop()


def main():
    """Función principal"""
    print("=" * 60)
    print("TEST INTERACTIVO: CU-24 Gestionar Observador del Estudiante")
    print("=" * 60)
    print()
    print("Este test permite verificar todos los aspectos del CU-24:")
    print("• Visualización interrumpible (PASO 5)")
    print("• Modo modificación con restricciones (PASO 6-8)")
    print("• Validaciones completas (PASO 11)")
    print("• Registro de cambios (PASO 13)")
    print()
    print("IMPORTANTE:")
    print("• Asegúrate de que el estudiante ID=2 existe")
    print("• El estudiante debe tener un observador asociado")
    print("• Puedes modificar los IDs en la interfaz")
    print()
    print("-" * 60)
    
    test = TestCU24()
    test.run()


if __name__ == "__main__":
    main()
