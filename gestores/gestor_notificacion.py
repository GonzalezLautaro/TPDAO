from datetime import datetime, timedelta
from data.database import Database
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cargar variables de entorno
load_dotenv()

class GestorNotificacion:
    def __init__(self):
        self.db = Database()
        
        # Credenciales Email
        self.email_sender = os.getenv('EMAIL_SENDER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
    def enviar_email(self, destinatario: str, asunto: str, mensaje: str) -> tuple:
        '''Envía email usando Gmail SMTP'''
        try:
            if not all([self.email_sender, self.email_password]):
                return False, 'Credenciales de email no configuradas en .env'
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = destinatario
            msg['Subject'] = asunto
            
            msg.attach(MIMEText(mensaje, 'plain', 'utf-8'))
            
            # Conectar a Gmail
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            
            # Enviar
            server.send_message(msg)
            server.quit()
            
            return True, f'Email enviado a {destinatario}'
            
        except Exception as e:
            return False, f'Error al enviar email: {str(e)}'
    
    def crear_notificacion_turno(self, id_turno: int, contacto_adicional: str = None) -> bool:
        '''Crea notificación automática para un turno'''
        try:
            if not self.db.conectar():
                return False

            # Obtener datos del turno y contactos del paciente
            query_turno = '''
            SELECT t.fecha, t.hora_inicio, t.id_paciente,
                   p.nombre, p.apellido
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            WHERE t.id_turno = %s
            '''
            resultado = self.db.obtener_registros(query_turno, (id_turno,))
            
            if not resultado:
                print(f'[WARNING] No se encontró el turno {id_turno}')
                return False
            
            turno = resultado[0]
            fecha_turno = turno['fecha']
            hora_turno = turno['hora_inicio']
            id_paciente = turno['id_paciente']
            
            # Obtener contactos del paciente (de la nueva tabla)
            query_contactos = '''
            SELECT tipo_contacto, valor_contacto, es_principal
            FROM Contactos_Paciente
            WHERE id_paciente = %s AND activo = TRUE
            ORDER BY es_principal DESC
            LIMIT 1
            '''
            contactos = self.db.obtener_registros(query_contactos, (id_paciente,))
            
            if not contactos and not contacto_adicional:
                print(f'[WARNING] Paciente {id_paciente} no tiene contactos registrados')
                return False
            
            # Usar contacto adicional o el principal de la BD
            if contacto_adicional:
                medio_envio = 'Email'
                valor_contacto = contacto_adicional
            else:
                contacto = contactos[0]
                medio_envio = contacto['tipo_contacto']
                valor_contacto = contacto['valor_contacto']
            
            # Combinar fecha y hora del turno
            fecha_hora_turno = datetime.combine(fecha_turno, 
                                                datetime.min.time().replace(
                                                    hour=hora_turno.seconds // 3600,
                                                    minute=(hora_turno.seconds % 3600) // 60
                                                ))
            
            # Programar notificación 24hs antes
            fecha_hora_envio = fecha_hora_turno - timedelta(hours=24)
            
            # Insertar notificación
            query_insert = '''
            INSERT INTO Notificacion 
            (id_turno, fecha_hora_envio, estado, medio_envio, intentos)
            VALUES (%s, %s, 'Pendiente', %s, 0)
            '''
            
            resultado = self.db.ejecutar_consulta(
                query_insert, 
                (id_turno, fecha_hora_envio, medio_envio)
            )
            
            if resultado:
                print(f'✓ Notificación {medio_envio} creada para turno {id_turno} - Envío: {fecha_hora_envio}')
                return True
            else:
                print(f'[ERROR] No se pudo crear notificación para turno {id_turno}')
                return False
                
        except Exception as e:
            print(f'[ERROR] crear_notificacion_turno: {str(e)}')
            return False
        finally:
            self.db.desconectar()

    def obtener_notificaciones_pendientes(self) -> list:
        '''Obtiene notificaciones pendientes'''
        try:
            if not self.db.conectar():
                return []

            query = '''
            SELECT n.id_notificacion, n.id_turno, n.medio_envio, n.intentos,
                   t.fecha, t.hora_inicio, t.id_paciente,
                   p.nombre, p.apellido,
                   m.nombre as medico_nombre, m.apellido as medico_apellido
            FROM Notificacion n
            JOIN Turno t ON n.id_turno = t.id_turno
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Medico m ON t.matricula = m.matricula
            WHERE n.estado = 'Pendiente'
              AND n.fecha_hora_envio <= NOW()
              AND n.intentos < 3
            ORDER BY n.fecha_hora_envio
            '''
            
            return self.db.obtener_registros(query)
            
        except Exception as e:
            print(f'[ERROR] obtener_notificaciones_pendientes: {str(e)}')
            return []
        finally:
            self.db.desconectar()

    def procesar_notificacion(self, notif: dict) -> bool:
        '''Procesa y envía una notificación individual'''
        try:
            id_notificacion = notif['id_notificacion']
            medio = notif['medio_envio']
            id_paciente = notif['id_paciente']
            
            # Obtener contacto del paciente
            if not self.db.conectar():
                return False
            
            query_contacto = '''
            SELECT valor_contacto FROM Contactos_Paciente
            WHERE id_paciente = %s AND tipo_contacto = %s AND activo = TRUE
            ORDER BY es_principal DESC LIMIT 1
            '''
            contactos = self.db.obtener_registros(query_contacto, (id_paciente, medio))
            self.db.desconectar()
            
            if not contactos:
                self._marcar_error(id_notificacion, f'Paciente sin contacto {medio}')
                return False
            
            destinatario = contactos[0]['valor_contacto']
            
            # Construir mensaje
            mensaje = self._construir_mensaje(notif)
            asunto = f'Recordatorio de Turno Médico - {notif["fecha"].strftime("%d/%m/%Y")}'
            
            # Enviar según medio
            if medio == 'Email':
                exito, resultado = self.enviar_email(destinatario, asunto, mensaje)
            else:
                exito = False
                resultado = f'Medio {medio} no implementado'
            
            # Actualizar estado
            if exito:
                self._marcar_enviado(id_notificacion)
                print(f'✓ Notificación {id_notificacion} enviada vía {medio}: {resultado}')
            else:
                self._incrementar_intento(id_notificacion, resultado)
                print(f'✗ Notificación {id_notificacion} falló: {resultado}')
            
            return exito
            
        except Exception as e:
            print(f'[ERROR] procesar_notificacion: {str(e)}')
            return False

    def _construir_mensaje(self, notif: dict) -> str:
        '''Construye el mensaje de notificación'''
        fecha = notif['fecha'].strftime('%d/%m/%Y')
        hora = str(notif['hora_inicio'])[:5]
        paciente = f"{notif['nombre']} {notif['apellido']}"
        medico = f"Dr/Dra. {notif['medico_nombre']} {notif['medico_apellido']}"
        
        mensaje = f'''
RECORDATORIO DE TURNO MÉDICO

Paciente: {paciente}
Fecha: {fecha}
Hora: {hora}
Médico: {medico}

Por favor, confirme su asistencia.

---
Sistema de Turnos Hospital DAO 2025
'''
        return mensaje.strip()

    def _marcar_enviado(self, id_notificacion: int):
        '''Marca notificación como enviada'''
        try:
            if not self.db.conectar():
                return
            
            query = '''
            UPDATE Notificacion 
            SET estado = 'Enviado', fecha_envio_real = NOW()
            WHERE id_notificacion = %s
            '''
            self.db.ejecutar_consulta(query, (id_notificacion,))
            
        except Exception as e:
            print(f'[ERROR] _marcar_enviado: {str(e)}')
        finally:
            self.db.desconectar()

    def _marcar_error(self, id_notificacion: int, motivo: str):
        '''Marca notificación como error'''
        try:
            if not self.db.conectar():
                return
            
            query = '''
            UPDATE Notificacion 
            SET estado = 'Error', motivo_error = %s, intentos = intentos + 1
            WHERE id_notificacion = %s
            '''
            self.db.ejecutar_consulta(query, (motivo, id_notificacion))
            
        except Exception as e:
            print(f'[ERROR] _marcar_error: {str(e)}')
        finally:
            self.db.desconectar()

    def _incrementar_intento(self, id_notificacion: int, motivo: str):
        '''Incrementa contador de intentos'''
        try:
            if not self.db.conectar():
                return
            
            query = '''
            UPDATE Notificacion 
            SET intentos = intentos + 1, motivo_error = %s
            WHERE id_notificacion = %s
            '''
            self.db.ejecutar_consulta(query, (motivo, id_notificacion))
            
        except Exception as e:
            print(f'[ERROR] _incrementar_intento: {str(e)}')
        finally:
            self.db.desconectar()
