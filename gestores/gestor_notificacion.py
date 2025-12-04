from datetime import datetime
from data.database import Database
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class GestorNotificacion:
    def __init__(self):
        self.db = Database()
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_from = os.getenv('TWILIO_PHONE_NUMBER')

    def crear_notificaciones_turno(self, id_turno, telefono_destino=None):
        '''
        Crea UNA notificación mínima y envía SMS por Twilio.
        '''
        if not self.db.conectar():
            print("[ERROR] No se pudo conectar a la base de datos")
            return False

        try:
            # Obtener datos del turno SIN JOINs
            query_turno = 'SELECT * FROM Turno WHERE id_turno = %s'
            turno = self.db.obtener_registro(query_turno, (id_turno,))
            print("[DEBUG] Turno:", turno)

            if not turno:
                print(f'[ERROR] No se encontró el turno {id_turno}')
                return False

            # Teléfono del paciente (puede venir por parámetro)
            telefono = telefono_destino or '+5491123456789'  # Cambia por el número real

            # Crear notificación mínima en la base
            fecha_envio = datetime.now()
            query_notif = '''
            INSERT INTO Notificacion (
                id_turno, medio_envio, fecha_hora_envio, estado, intentos
            ) VALUES (%s, 'SMS', %s, 'Pendiente', 0)
            '''
            self.db.ejecutar_consulta(query_notif, (id_turno, fecha_envio))

            # Enviar SMS por Twilio
            mensaje = f"Recordatorio de turno médico: {turno['fecha']} a las {turno['hora_inicio']}"
            try:
                client = Client(self.twilio_sid, self.twilio_token)
                sms = client.messages.create(
                    body=mensaje,
                    from_=self.twilio_from,
                    to=telefono
                )
                print(f'✓ SMS enviado a {telefono}: SID {sms.sid}')
            except Exception as e:
                print(f'[ERROR] al enviar SMS: {str(e)}')

            print(f'✓ Notificación SMS creada y enviada para turno {id_turno}')
            return True

        except Exception as e:
            print(f'[ERROR] al crear notificación: {str(e)}')
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.db.desconectar()