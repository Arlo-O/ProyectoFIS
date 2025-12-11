from .usuario import Usuario


class Directivo(Usuario):
    def __init__(self, id_directivo: int, cargo: str = "", area_responsable: str = ""):
        super().__init__()
        self.__id_directivo = id_directivo
        self.__cargo = cargo
        self.__area_responsable = area_responsable

    @property
    def id_directivo(self) -> int:
        return self.__id_directivo

    @property
    def cargo(self) -> str:
        return self.__cargo

    @cargo.setter
    def cargo(self, value: str) -> None:
        self.__cargo = value

    @property
    def area_responsable(self) -> str:
        return self.__area_responsable

    @area_responsable.setter
    def area_responsable(self, value: str) -> None:
        self.__area_responsable = value
