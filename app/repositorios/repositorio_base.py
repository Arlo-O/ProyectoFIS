from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')


class RepositorioBase(Generic[T]):
    """Clase base para todos los repositorios"""

    def __init__(self, db: Session, modelo: type):
        self.db = db
        self.modelo = modelo

    def crear(self, obj: T) -> T:
        """Crea un nuevo registro"""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def obtener_por_id(self, id: int) -> Optional[T]:
        """Obtiene un registro por ID"""
        return self.db.query(self.modelo).filter(self.modelo.id == id).first()

    def obtener_todos(self) -> List[T]:
        """Obtiene todos los registros"""
        return self.db.query(self.modelo).all()

    def actualizar(self, id: int, obj: T) -> Optional[T]:
        """Actualiza un registro"""
        db_obj = self.obtener_por_id(id)
        if db_obj:
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def eliminar(self, id: int) -> bool:
        """Elimina un registro"""
        db_obj = self.obtener_por_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False

    def filtrar(self, **kwargs) -> List[T]:
        """Filtra registros por atributos"""
        query = self.db.query(self.modelo)
        for key, value in kwargs.items():
            if hasattr(self.modelo, key):
                query = query.filter(getattr(self.modelo, key) == value)
        return query.all()
