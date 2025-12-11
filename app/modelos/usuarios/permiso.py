from typing import Optional


class Permiso:
    def __init__(self, id_permiso: int, nombre_permiso: str, descripcion: str = ""):
        self.__id_permiso = id_permiso
        self.__nombre_permiso = nombre_permiso
        self.__descripcion = descripcion

    @property
    def id_permiso(self) -> int:
        return self.__id_permiso

    @property
    def nombre_permiso(self) -> str:
        return self.__nombre_permiso

    @nombre_permiso.setter
    def nombre_permiso(self, value: str) -> None:
        self.__nombre_permiso = value

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, value: str) -> None:
        self.__descripcion = value
