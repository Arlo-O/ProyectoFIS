from .usuario import Usuario


class Administrador(Usuario):
    def __init__(self, id_administrador: int):
        super().__init__()
        self.__id_administrador = id_administrador

    @property
    def id_administrador(self) -> int:
        return self.__id_administrador
