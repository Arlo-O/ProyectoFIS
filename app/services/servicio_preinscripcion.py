# 🔧 Servicio de Preinscripción
from typing import Dict, Tuple, List
import json
import os
from datetime import datetime
from pathlib import Path
from ..core.preinscripcion.modelo_preinscripcion import IntentoFallo, FormularioPreinscripcion


class ServicioIntentosFallidos:
    """Servicio para persistir y gestionar intentos fallidos de preinscripción"""
    
    def __init__(self):
        # Crear directorio de almacenamiento si no existe
        self.directorio_datos = Path.home() / ".proyectofis" / "preinscripcion"
        self.directorio_datos.mkdir(parents=True, exist_ok=True)
        self.archivo_intentos = self.directorio_datos / "intentos_fallidos.json"
    
    def obtener_intentos_usuario(self, identificador: str = "usuario_anonimo") -> List[IntentoFallo]:
        """Obtiene todos los intentos fallidos del usuario"""
        if not self.archivo_intentos.exists():
            return []
        
        try:
            with open(self.archivo_intentos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            intentos = [IntentoFallo(**intento) for intento in datos.get(identificador, [])]
            return intentos
        except Exception as e:
            print(f"Error al leer intentos: {e}")
            return []
    
    def contar_intentos_hoy(self, identificador: str = "usuario_anonimo") -> int:
        """Cuenta cuántos intentos fallidos ha habido hoy"""
        intentos = self.obtener_intentos_usuario(identificador)
        hoy = datetime.now().date()
        
        intentos_hoy = [
            i for i in intentos 
            if datetime.fromisoformat(i.fecha_hora).date() == hoy
        ]
        
        return len(intentos_hoy)
    
    def registrar_intento_fallido(self, 
                                  numero_error: int, 
                                  campo_errores: Dict[str, str],
                                  identificador: str = "usuario_anonimo") -> IntentoFallo:
        """Registra un intento fallido"""
        
        intento = IntentoFallo(
            numero_error=numero_error,
            campo_errores=campo_errores
        )
        
        # Leer intentos existentes
        try:
            with open(self.archivo_intentos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = {}
        
        # Agregar nuevo intento
        if identificador not in datos:
            datos[identificador] = []
        
        datos[identificador].append(intento.to_dict())
        
        # Guardar
        try:
            with open(self.archivo_intentos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar intento: {e}")
        
        return intento
    
    def limpiar_intentos_usuario(self, identificador: str = "usuario_anonimo"):
        """Limpia los intentos fallidos del usuario actual"""
        try:
            with open(self.archivo_intentos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            if identificador in datos:
                del datos[identificador]
            
            with open(self.archivo_intentos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al limpiar intentos: {e}")


class ServicioPreinscripcion:
    """Servicio de validación y persistencia de preinscripciones"""
    
    def __init__(self):
        self.servicio_intentos = ServicioIntentosFallidos()
    
    def guardar_preinscripcion(self, formulario: FormularioPreinscripcion) -> Tuple[bool, str]:
        """Guarda una preinscripción completada"""
        try:
            directorio = Path.home() / ".proyectofis" / "preinscripcion"
            directorio.mkdir(parents=True, exist_ok=True)
            
            archivo = directorio / f"preinscripcion_{datetime.now().isoformat().replace(':', '-')}.json"
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(formulario.to_dict(), f, ensure_ascii=False, indent=2)
            
            return True, "Preinscripción guardada exitosamente"
        except Exception as e:
            return False, f"Error al guardar preinscripción: {str(e)}"
    
    def obtener_contador_intentos(self, identificador: str = "usuario_anonimo") -> int:
        """Obtiene el número de intentos fallidos hoy"""
        return self.servicio_intentos.contar_intentos_hoy(identificador)
    
    def registrar_error(self, 
                       errores: Dict[str, str],
                       identificador: str = "usuario_anonimo") -> IntentoFallo:
        """Registra un error de validación"""
        contador = self.obtener_contador_intentos(identificador) + 1
        return self.servicio_intentos.registrar_intento_fallido(
            contador, 
            errores, 
            identificador
        )
