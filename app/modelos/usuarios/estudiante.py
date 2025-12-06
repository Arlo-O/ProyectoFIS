from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from .usuario import Usuario
from .rol import Rol

if TYPE_CHECKING:
    from ..academico.grupo import Grupo
    from .acudiente import Acudiente
    from ..academico.hojaVidaAcademica import HojaVidaAcademica
    from ..academico.observador import Observador
    from ..logros.evaluacionLogro import EvaluacionLogro
    from ..logros.boletin import Boletin

class Estudiante(Usuario):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, correoElectronico: str, rol: Rol, contrasena: str,
                 idEstudiante: int = None, fechaIngreso: datetime = None, codigoMatricula: str = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono,
                         correoElectronico, rol, contrasena)
        self.__idEstudiante: int = idEstudiante
        self.__fechaIngreso: datetime = fechaIngreso
        self.__codigoMatricula: str = codigoMatricula
        self.__acudientes: List['Acudiente'] = []
        self.__grupo: Optional['Grupo'] = None
        self.__hojaVida: Optional['HojaVidaAcademica'] = None
        self.__observador: Optional['Observador'] = None
        self.__logrosObtenidos: List['EvaluacionLogro'] = []

    @property
    def idEstudiante(self) -> int:
        return self.__idEstudiante

    @property
    def fechaIngreso(self) -> datetime:
        return self.__fechaIngreso

    @property
    def codigoMatricula(self) -> str:
        return self.__codigoMatricula

    @property
    def grupo(self) -> Optional['Grupo']:
        return self.__grupo

    @grupo.setter
    def grupo(self, nuevoGrupo: 'Grupo') -> None:
        self.__grupo = nuevoGrupo

    def obtenerAcudientes(self) -> List['Acudiente']:
        return self.__acudientes.copy()

    def obtenerBoletinActual(self) -> Optional['Boletin']:
        # Logic to get current bulletin
        return None

    def obtenerHistoriaAcademica(self) -> List['EvaluacionLogro']:
        return self.__logrosObtenidos.copy()

    def agregarAcudiente(self, acudiente: 'Acudiente') -> None:
        if len(self.__acudientes) < 2 and acudiente not in self.__acudientes:
            self.__acudientes.append(acudiente)

    def eliminarAcudiente(self, acudiente: 'Acudiente') -> None:
        if acudiente in self.__acudientes:
            self.__acudientes.remove(acudiente)

    def agregarCalificacion(self, evaluacion: 'EvaluacionLogro') -> None:
        self.__logrosObtenidos.append(evaluacion)

    def eliminarCalificacion(self, evaluacion: 'EvaluacionLogro') -> None:
        if evaluacion in self.__logrosObtenidos:
            self.__logrosObtenidos.remove(evaluacion)