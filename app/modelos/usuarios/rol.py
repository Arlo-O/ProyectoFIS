from typing import List

from app.modelos.usuarios.permiso import Permiso


class Rol:
    def __init__(self, id_rol: int, nombre_rol: str, descripcion_rol: str = ""):
        self.__id_rol = id_rol
        self.__nombre_rol = nombre_rol
        self.__descripcion_rol = descripcion_rol
        self.__permisos: List['Permiso'] = []

    @property
    def id_rol(self) -> int:
        return self.__id_rol

    @property
    def nombre_rol(self) -> str:
        return self.__nombre_rol

    @nombre_rol.setter
    def nombre_rol(self, value: str) -> None:
        self.__nombre_rol = value

    @property
    def descripcion_rol(self) -> str:
        return self.__descripcion_rol

    @descripcion_rol.setter
    def descripcion_rol(self, value: str) -> None:
        self.__descripcion_rol = value

    @property
    def permisos(self) -> List['Permiso']:
        return self.__permisos.copy()
