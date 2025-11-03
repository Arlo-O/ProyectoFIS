from abc import ABC, abstractmethod

class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento: str, datos: dict) -> None:
        pass

class Observable:
    def __init__(self):
        self.__observadores: list = []

    def agregarObservador(self, observador: Observador) -> None:
        if observador not in self.__observadores:
            self.__observadores.append(observador)

    def removerObservador(self, observador: Observador) -> None:
        try:
            self.__observadores.remove(observador)
        except ValueError:
            pass

    def notificar(self, evento: str, datos: dict = None) -> None:
        for obs in self.__observadores:
            try:
                obs.actualizar(evento, datos or {})
            except Exception:
                pass