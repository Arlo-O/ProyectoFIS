from datetime import datetime
from .rol import Rol
from .persona import Persona

class Usuario(Persona):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, correoElectronico: str, rol: Rol, contrasena: str, idUsuario: int = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono)
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
    
    @idUsuario.setter
    def idUsuario(self, idUsuario: int) -> None:
        self.__idUsuario = idUsuario

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
    def ultimoIngreso(self) -> datetime:
        return self.__ultimoIngreso
    
    @property
    def contrasenaEncriptada(self) -> str:
        return self.__contrasenaEncriptada

    @contrasenaEncriptada.setter
    def contrasenaEncriptada(self, nuevaContrasena: str) -> None:
        self.__contrasenaEncriptada = nuevaContrasena

    @ultimoIngreso.setter
    def ultimoIngreso(self, nuevoIngreso: datetime) -> None:
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
        
    def autenticar(self, nombreUsuario: str, contrasena: str) -> bool:
        # Assuming nombreUsuario can be email or specific username if added.
        # Dictionary says 'nombreUsuario' param.
        return self.__correoElectronico == nombreUsuario and self.__contrasenaEncriptada == contrasena
        
    def recuperarContrasena(self, correoElectronico: str) -> None:
        # Logic to send recovery email
        pass

    def cambiarContrasena(self, contrasenaNueva: str) -> None:
        self.__contrasenaEncriptada = contrasenaNueva