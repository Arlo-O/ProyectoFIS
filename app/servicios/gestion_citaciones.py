from typing import List, Optional
from datetime import datetime
from app.infraestructura.uow import UnitOfWork
from app.infraestructura.notificaciones import ServicioNotificaciones
from app.modelos.gestion.citacion import Citacion

class ServicioGestionCitaciones:
    def __init__(self):
        self.uow = UnitOfWork()
        self.notificaciones = ServicioNotificaciones()

    def generar_citacion(self, fecha: datetime, motivo: str, descripcion: str, lugar: str, 
                         correos: List[str], id_remitente: int) -> Optional[Citacion]:
        with self.uow:
            remitente = self.uow.directivos.get(id_remitente)
            if remitente:
                citacion = Citacion(
                    idCitacion=None,
                    fechaProgramada=fecha,
                    correoDestinatarios=correos,
                    motivo=motivo,
                    descripcion=descripcion,
                    lugar=lugar,
                    remitente=remitente
                )
                self.uow.citaciones.add(citacion)
                self.uow.commit()
                
                self.notificaciones.enviar_correo(
                    destinatarios=correos,
                    asunto=f"Citación: {motivo}",
                    contenido=f"Se le cita para el {fecha} en {lugar}. Detalles: {descripcion}"
                )
                
                return citacion
            return None

    def consultar_historial_citaciones(self, id_estudiante: int) -> List[Citacion]:
        with self.uow:
            return self.uow.citaciones.get_all()
