from datetime import datetime
from typing import Optional
from .persona import Persona
from .rol import Rol


class Usuario(Persona):
    def __init__(self, id_usuario: int, contrasena: str, correo_electronico: str, 
                 id_rol: Optional[int] = None, activo: bool = True,
                 fecha_creacion: Optional[datetime] = None, ultimo_ingreso: Optional[datetime] = None):
        super().__init__()
        self.__id_usuario = id_usuario
        self.__contrasena = contrasena
        self.__correo_electronico = correo_electronico
        self.__id_rol = id_rol
        self.__activo = activo
        self.__fecha_creacion = fecha_creacion
        self.__ultimo_ingreso = ultimo_ingreso

    @property
    def id_usuario(self) -> int:
        return self.__id_usuario

    @property
    def contrasena(self) -> str:
        return self.__contrasena

    @property
    def correo_electronico(self) -> str:
        return self.__correo_electronico

    @correo_electronico.setter
    def correo_electronico(self, value: str) -> None:
        self.__correo_electronico = value

    @property
    def id_rol(self) -> Optional[int]:
        return self.__id_rol

    @property
    def activo(self) -> bool:
        return self.__activo

    @activo.setter
    def activo(self, value: bool) -> None:
        self.__activo = value

    @property
    def fecha_creacion(self) -> Optional[datetime]:
        return self.__fecha_creacion

    @property
    def ultimo_ingreso(self) -> Optional[datetime]:
        return self.__ultimo_ingreso

    @ultimo_ingreso.setter
    def ultimo_ingreso(self, value: Optional[datetime]) -> None:
        self.__ultimo_ingreso = value
