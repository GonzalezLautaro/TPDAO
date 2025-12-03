from datetime import datetime, timedelta
from data.database import Database
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GestorNotificacion:
    def __init__(self):
        self.db = Database()
        
        # Credenciales Twilio desde .env
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
    def crear_notificacion_turno(self, id_turno: int, telefono_paciente: str = None) -> bool:
        """
        Crea una notificación automática para un turno programado.
        Se programa para 24hs antes del turno.
        """
        try:
            if not self.db.conectar():
                return False

            # Obtener datos del turno
            query_turno = """
            SELECT t.fecha, t.hora_inicio, p.telefono
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            WHERE t.id_turno = %s
            """
            resultado = self.db.obtener_registros(query_turno, (id_turno,))
            
            if not resultado:
                print(f"[WARNING] No se encontró el turno {id_turno}")
                return False
            
            turno = resultado[0]
            fecha_turno = turno['fecha']
            hora_turno = turno['hora_inicio']
            telefono = telefono_paciente or turno['telefono']
            email = None  # Email no disponible en tabla Paciente
            
            # Combinar fecha y hora del turno
            fecha_hora_turno = datetime.combine(fecha_turno, 
                                                datetime.min.time().replace(
                                                    hour=hora_turno.seconds // 3600,
                                                    minute=(hora_turno.seconds % 3600) // 60
                                                ))
            
            # Programar notificación 24hs antes
            fecha_hora_envio = fecha_hora_turno - timedelta(hours=24)
            
            # Determinar medio de envío
            medio_envio = 'SMS' if telefono else 'Email' if email else None
            
            if not medio_envio:
                print(f"[WARNING] Turno {id_turno} no tiene teléfono ni email")
                return False
            
            # Insertar notificación
            query_insert = """
            INSERT INTO Notificacion 
            (id_turno, fecha_hora_envio, estado, medio_envio, intentos)
            VALUES (%s, %s, 'Pendiente', %s, 0)
            """
            
            resultado = self.db.ejecutar_consulta(
                query_insert, 
                (id_turno, fecha_hora_envio, medio_envio)
            )
            
            if resultado:
                print(f"✓ Notificación creada para turno {id_turno} - Envío: {fecha_hora_envio}")
                return True
            else:
                print(f"[ERROR] No se pudo crear notificación para turno {id_turno}")
                return False
                
        except Exception as e:
            print(f"[ERROR] crear_notificacion_turno: {str(e)}")
            return False
        finally:
            self.db.desconectar()

    def obtener_notificaciones_pendientes(self) -> list:
        """Obtiene notificaciones pendientes que deben enviarse ahora"""
        try:
            if not self.db.conectar():
                return []

            query = """
            SELECT n.id_notificacion, n.id_turno, n.medio_envio, n.intentos,
                   t.fecha, t.hora_inicio,
                   p.nombre, p.apellido, p.telefono,
                   m.nombre as medico_nombre, m.apellido as medico_apellido
            FROM Notificacion n
            JOIN Turno t ON n.id_turno = t.id_turno
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Medico m ON t.matricula = m.matricula
            WHERE n.estado = 'Pendiente'
              AND n.fecha_hora_envio <= NOW()
              AND n.intentos < 3
            ORDER BY n.fecha_hora_envio
            """
            
            return self.db.obtener_registros(query)
            
        except Exception as e:
            print(f"[ERROR] obtener_notificaciones_pendientes: {str(e)}")
            return []
        finally:
            self.db.desconectar()

    def enviar_sms_twilio(self, telefono: str, mensaje: str) -> tuple:
        """Envía SMS usando Twilio"""
        try:
            # Validar credenciales
            if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
                return False, "Credenciales de Twilio no configuradas en .env"
            
            # Importar Twilio
            try:
                from twilio.rest import Client
            except ImportError:
                return False, "Twilio no instalado. Ejecuta: pip install twilio"
            
            # Formatear teléfono
            if not telefono.startswith('+'):
                telefono = '+54' + telefono  # Código Argentina
            
            # Enviar SMS
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            message = client.messages.create(
                body=mensaje,
                from_=self.twilio_phone_number,
                to=telefono
            )
            
            return True, f"SMS enviado. SID: {message.sid}"
            
        except Exception as e:
            return False, f"Error Twilio: {str(e)}"

    def procesar_notificacion(self, notif: dict) -> bool:
        """Procesa y envía una notificación individual"""
        try:
            id_notificacion = notif['id_notificacion']
            medio = notif['medio_envio']
            
            # Construir mensaje
            mensaje = self._construir_mensaje(notif)
            
            # Enviar según medio
            if medio == 'SMS':
                telefono = notif['telefono']
                if not telefono:
                    self._marcar_error(id_notificacion, "Paciente sin teléfono")
                    return False
                
                exito, resultado = self.enviar_sms_twilio(telefono, mensaje)
                
            elif medio == 'Email':
                # Implementación futura
                exito = False
                resultado = "Envío de Email no implementado"
            else:
                exito = False
                resultado = "Medio de envío desconocido"
            
            # Actualizar estado
            if exito:
                self._marcar_enviado(id_notificacion)
                print(f"✓ Notificación {id_notificacion} enviada: {resultado}")
            else:
                self._incrementar_intento(id_notificacion, resultado)
                print(f"✗ Notificación {id_notificacion} falló: {resultado}")
            
            return exito
            
        except Exception as e:
            print(f"[ERROR] procesar_notificacion: {str(e)}")
            return False

    def _construir_mensaje(self, notif: dict) -> str:
        """Construye el mensaje de notificación"""
        fecha = notif['fecha'].strftime('%d/%m/%Y')
        hora = str(notif['hora_inicio'])[:5]
        paciente = f"{notif['nombre']} {notif['apellido']}"
        medico = f"Dr/Dra. {notif['medico_nombre']} {notif['medico_apellido']}"
        
        mensaje = f"""
Recordatorio de Turno Médico

Paciente: {paciente}
Fecha: {fecha}
Hora: {hora}
Médico: {medico}

Por favor, confirme su asistencia.
"""
        return mensaje.strip()

    def _marcar_enviado(self, id_notificacion: int):
        """Marca notificación como enviada"""
        try:
            if not self.db.conectar():
                return
            
            query = """
            UPDATE Notificacion 
            SET estado = 'Enviado', 
                fecha_envio_real = NOW()
            WHERE id_notificacion = %s
            """
            self.db.ejecutar_consulta(query, (id_notificacion,))
            
        except Exception as e:
            print(f"[ERROR] _marcar_enviado: {str(e)}")
        finally:
            self.db.desconectar()

    def _marcar_error(self, id_notificacion: int, motivo: str):
        """Marca notificación como error"""
        try:
            if not self.db.conectar():
                return
            
            query = """
            UPDATE Notificacion 
            SET estado = 'Error', 
                motivo_error = %s,
                intentos = intentos + 1
            WHERE id_notificacion = %s
            """
            self.db.ejecutar_consulta(query, (motivo, id_notificacion))
            
        except Exception as e:
            print(f"[ERROR] _marcar_error: {str(e)}")
        finally:
            self.db.desconectar()

    def _incrementar_intento(self, id_notificacion: int, motivo: str):
        """Incrementa contador de intentos"""
        try:
            if not self.db.conectar():
                return
            
            query = """
            UPDATE Notificacion 
            SET intentos = intentos + 1,
                motivo_error = %s
            WHERE id_notificacion = %s
            """
            self.db.ejecutar_consulta(query, (motivo, id_notificacion))
            
        except Exception as e:
            print(f"[ERROR] _incrementar_intento: {str(e)}")
        finally:
            self.db.desconectar()
