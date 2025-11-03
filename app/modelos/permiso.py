class Permiso:
    def __init__(self, idPermiso: int, nombre: str, descripcion: str):
        self.__idPermiso = idPermiso
        self.__nombre = nombre
        self.__descripcion = descripcion

    @property
    def idPermiso(self) -> int:
        return self.__idPermiso

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def descripcion(self) -> str:
        return self.__descripcion
    
    @nombre.setter
    def nombre(self, nuevoNombre: str)-> None:
        self.__nombre = nuevoNombre

    @descripcion.setter
    def actualizarDescripcion(self, nuevaDescripcion: str) -> None:
        self.__descripcion = nuevaDescripcion

    def __str__(self):
        return f"Permiso(ID: {self.__idPermiso}, Nombre: {self.__nombre})"