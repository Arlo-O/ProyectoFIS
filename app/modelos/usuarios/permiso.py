class Permiso:
    def __init__(self, idPermiso: int, nombrePermiso: str, descripcion: str):
        self.__idPermiso = idPermiso
        self.__nombrePermiso = nombrePermiso
        self.__descripcion = descripcion

    @property
    def idPermiso(self) -> int:
        return self.__idPermiso

    @property
    def nombrePermiso(self) -> str:
        return self.__nombrePermiso

    @property
    def descripcion(self) -> str:
        return self.__descripcion
    
    @nombrePermiso.setter
    def nombrePermiso(self, nuevoNombre: str)-> None:
        self.__nombrePermiso = nuevoNombre

    def actualizarDescripcion(self, desc: str) -> None:
        self.__descripcion = desc

    def __str__(self):
        return f"Permiso(ID: {self.__idPermiso}, Nombre: {self.__nombrePermiso})"