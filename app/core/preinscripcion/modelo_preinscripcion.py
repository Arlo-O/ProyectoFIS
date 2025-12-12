# 📦 Modelo de Preinscripción
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class IntentoFallo:
    """Representa un intento fallido de envío de formulario"""
    id_intento: Optional[int] = None
    fecha_hora: str = None
    numero_error: int = 0
    campo_errores: Dict[str, str] = None
    dispositivo: str = "desktop"
    
    def __post_init__(self):
        if self.fecha_hora is None:
            self.fecha_hora = datetime.now().isoformat()
        if self.campo_errores is None:
            self.campo_errores = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id_intento': self.id_intento,
            'fecha_hora': self.fecha_hora,
            'numero_error': self.numero_error,
            'campo_errores': self.campo_errores,
            'dispositivo': self.dispositivo
        }


@dataclass
class DatosEstudiante:
    """Datos del estudiante"""
    nombre: str
    tipo_id: str
    numero_id: str
    fecha_nacimiento: str
    genero: str
    grado: str


@dataclass
class DatosAcudiente:
    """Datos de un acudiente"""
    nombre: str
    cedula: str
    telefono: str
    email: str
    direccion: str
    parentesco: str


@dataclass
class DatosInformacionMedica:
    """Información médica del estudiante"""
    alergias: str = ""
    medicamentos: str = ""
    colegio_anterior: str = ""


@dataclass
class FormularioPreinscripcion:
    """Modelo principal del formulario de preinscripción"""
    id_solicitud: Optional[int] = None
    fecha_solicitud: str = None
    estudiante: Optional[DatosEstudiante] = None
    acudiente_principal: Optional[DatosAcudiente] = None
    acudiente_secundario: Optional[DatosAcudiente] = None
    informacion_medica: Optional[DatosInformacionMedica] = None
    acepto_terminos: bool = False
    estado: str = "pendiente"  # pendiente, procesada, rechazada
    
    def __post_init__(self):
        if self.fecha_solicitud is None:
            self.fecha_solicitud = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id_solicitud': self.id_solicitud,
            'fecha_solicitud': self.fecha_solicitud,
            'estudiante': asdict(self.estudiante) if self.estudiante else None,
            'acudiente_principal': asdict(self.acudiente_principal) if self.acudiente_principal else None,
            'acudiente_secundario': asdict(self.acudiente_secundario) if self.acudiente_secundario else None,
            'informacion_medica': asdict(self.informacion_medica) if self.informacion_medica else None,
            'acepto_terminos': self.acepto_terminos,
            'estado': self.estado
        }
