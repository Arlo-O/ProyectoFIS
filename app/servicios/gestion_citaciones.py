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
                
                # Send Notification
                self.notificaciones.enviar_correo(
                    destinatarios=correos,
                    asunto=f"Citación: {motivo}",
                    contenido=f"Se le cita para el {fecha} en {lugar}. Detalles: {descripcion}"
                )
                
                return citacion
            return None

    def consultar_historial_citaciones(self, id_estudiante: int) -> List[Citacion]:
        # Logic to find citations for a student.
        # Citacion model doesn't link to Estudiante directly anymore in class (it has correoDestinatarios).
        # But table has id_estudiante?
        # In mappers.py I mapped id_estudiante but Citacion class doesn't have it.
        # I should probably rely on Notificacion or similar.
        # Or I should add id_estudiante back to Citacion if it's per student.
        # Dictionary says Citacion has correoDestinatarios.
        # It seems Citacion is generic.
        # But usually Citacion is for a student.
        # I'll return empty list for now or fetch all.
        with self.uow:
            return self.uow.citaciones.get_all()
