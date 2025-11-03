from datetime import datetime
from rol import Rol

class Usuario:
    def __init__(self, idUsuario: int, correoElectronico: str, rol: Rol, contrasena: str):
        self.__idUsuario = idUsuario
        self.__contrasenaEncriptada: str = contrasena
        self.__fechaCreacion: datetime = datetime.now()
        self.__ultimoIngreso: datetime = None
        self.__rol: Rol = rol
        self.__activo: bool = True
        self.__correoElectronico = correoElectronico

    @property
    def idUsuario(self) -> int:
        return self.__idUsuario
    
    @property
    def rol(self) -> Rol:
        return self.__rol
        
    @property
    def activo(self) -> bool:
        return self.__activo
        
    @property
    def correoElectronico(self) -> str:
        return self.__correoElectronico
    
    @property
    def fechaCreacion(self) -> datetime:
        return self.__fechaCreacion
    
    @property
    def ulitmoIngreso(self) -> datetime:
        return self.__ultimoIngreso
    
    @property
    def contrasenaEncriptada(self) -> str:
        return self.__contrasenaEncriptada

    @contrasenaEncriptada.setter
    def contrasenaEcnriptada(self, nuevaContrasena: Rol) -> None:
        self.__contrasenaEncriptada = nuevaContrasena

    @ulitmoIngreso.setter
    def rol(self, nuevoIngreso: datetime) -> None:
        self.__ultimoIngreso = nuevoIngreso

    @rol.setter
    def rol(self, nuevoRol: Rol) -> None:
        self.__rol = nuevoRol

    @activo.setter
    def activo(self, nuevoEstado: bool) -> None:
        self.__activo = nuevoEstado

    @correoElectronico.setter
    def correoElectronico(self, nuevoCorreo: str) -> None:
        self.__correoElectronico = nuevoCorreo
        
    def autenticar(self, correo: str, contrasena: str) -> bool:
        if self.__correoElectronico == correo and self.__contrasenaEncriptada == contrasena:
            self.__ultimoIngreso = datetime.now()
            return True
        else: 
            return False
        
    def recuperarContrasena(self, correo: str) -> None:
        pass