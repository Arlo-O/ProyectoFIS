from usuario import Usuario

class Adminitrador (Usuario):
    def __init__(self, idUsuario, correoElectronico, rol, contrasena, idAdmin : int):
        super().__init__(idUsuario, correoElectronico, rol, contrasena)
        self._idAdmin : int = idAdmin
    
    def crearUsuario(self, idUsuario: int, correoElectronico: str, rol, contrasena: str) -> Usuario:
        nuevo_usuario = Usuario(idUsuario, correoElectronico, rol, contrasena)
        return nuevo_usuario
    
    def inhabilitarUsuario(self, usuario : Usuario):
        usuario.activo = False