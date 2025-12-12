from typing import List, Optional, Tuple
from datetime import datetime
import logging
from app.data.uow import uow
from app.services.notificaciones import ServicioNotificaciones
from app.core.gestion.citacion import Citacion
from app.core.usuarios.directivo import Directivo

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServicioGestionCitaciones:
    def __init__(self, notificaciones: ServicioNotificaciones):
        self.notificaciones = notificaciones

    def generar_citacion(self, fecha: datetime, motivo: str, descripcion: str, lugar: str, 
                        correos: List[str], id_remitente: int) -> Tuple[bool, str, Optional[Citacion]]:
        try:
            with uow() as uow_instance:
                remitente = uow_instance.directivos.get(id_remitente)
                if not remitente:
                    logger.warning(f"Directivo remitente no encontrado: {id_remitente}")
                    return (False, "Directivo remitente no encontrado", None)
                
                citacion = Citacion(
                    id_citacion=None,
                    fecha_programada=fecha,
                    correo_destinatarios=correos,
                    motivo=motivo,
                    descripcion=descripcion,
                    lugar=lugar,
                    id_remitente=remitente.id_directivo
                )
                
                uow_instance.citaciones.add(citacion)
                
                # El ID se genera después del commit automático del Unit of Work
                logger.info("Citación creada, pendiente de commit")
                
                # Notificación DESPUÉS de que el Unit of Work haga commit automáticamente
                try:
                    self.notificaciones.enviar_correo(
                        destinatarios=correos,
                        asunto=f"Citación: {motivo}",
                        contenido=f"Se le cita para el {fecha.strftime('%d/%m/%Y %H:%M')} en {lugar}. Detalles: {descripcion}"
                    )
                except Exception as email_error:
                    logger.error(f"Error enviando correo: {email_error}")
                    # No fallar toda la operación si el correo falla
                
                # El commit ocurre aquí automáticamente al salir del with
                return (True, "Citación generada y enviada correctamente", citacion)
                
        except Exception as e:
            logger.error(f"Error generando citación: {e}")
            return (False, f"Error interno: {str(e)}", None)

    def consultar_historial_citaciones(self, id_directivo: Optional[int] = None) -> List[Citacion]:
        with uow() as uow_instance:
            if id_directivo:
                # Filtrar por directivo (historial de citaciones generadas)
                return uow_instance.citaciones.get_by_directivo(id_directivo)
            return uow_instance.citaciones.get_all()

    def consultar_citaciones_pendientes(self, correos: List[str]) -> List[Citacion]:
        """Citaciones pendientes para correos específicos"""
        with uow() as uow_instance:
            # Lógica para filtrar citaciones pendientes por correos
            return uow_instance.citaciones.get_by_correo(correos[0])
