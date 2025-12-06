from .usuario import Usuario
from .rol import Rol
from datetime import datetime

class Administrador(Usuario):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, correoElectronico: str, rol: Rol, contrasena: str,
                 idAdministrador: int = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono,
                         correoElectronico, rol, contrasena)
        self.__idAdministrador: int = idAdministrador
    
    @property
    def idAdministrador(self) -> int:
        return self.__idAdministrador

    @idAdministrador.setter
    def idAdministrador(self, nuevoId: int) -> None:
        self.__idAdministrador = nuevoId

    def crearUsuario(self, correo: str, rol: Rol) -> Usuario:
        # Logic to create user
        # This returns a new Usuario instance but doesn't persist it here (Service layer does that)
        # Placeholder
        return None
    
    def inhabilitarUsuario(self, usuario: Usuario) -> None:
        usuario.activo = False