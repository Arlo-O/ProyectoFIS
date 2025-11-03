from permiso import Permiso
from typing import List

class Rol:
    def __init__(self, idRol: int, nombreRol: str, descripcionRol: str):
        self.__idRol = idRol
        self.__nombreRol = nombreRol
        self.__descripcionRol = descripcionRol
        self.__permisos: List[Permiso] = []

    @property
    def idRol(self) -> int:
        return self.__idRol

    @property
    def nombreRol(self) -> str:
        return self.__nombreRol

    @property
    def descripcionRol(self) -> str:
        return self.__descripcionRol

    @property
    def permisos(self) -> List[Permiso]:
        return self.__permisos.copy()

    @nombreRol.setter
    def nombreRol(self, nuevoNombre: str) -> None:
        self.__nombreRol = nuevoNombre

    @descripcionRol.setter
    def descripcionRol(self, nuevaDescripcion: str) -> None:
        self.__descripcionRol = nuevaDescripcion

    def agregarPermiso(self, permiso: Permiso) -> None:
        if permiso not in self.__permisos:
            self.__permisos.append(permiso)

    def eliminarPermiso(self, permiso: Permiso) -> None:
        try:
            self.__permisos.remove(permiso)
        except ValueError:
            print(f"ERROR: Permiso '{permiso.nombre}' no encontrado.")

    def __str__(self):
        num_permisos = len(self.__permisos)
        return f"Rol(ID: {self.__idRol}, Nombre: {self.__nombreRol}, Permisos: {num_permisos})"