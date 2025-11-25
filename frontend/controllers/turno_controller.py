from datetime import datetime, timedelta
import sys, os

# asegurar tpdao en sys.path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

# importar tu backend real
from gestores.gestor_turno import GestorTurno


class TurnoController:
    def __init__(self):
        self.gestor = GestorTurno()

    def programar(self, dni, matricula, fecha_str):
        """
        dni = id_paciente (int)
        matricula = matrícula del médico (int)
        fecha_str = "YYYY-MM-DD HH:MM"
        """
        if not dni or not matricula or not fecha_str:
            return False, "Faltan datos"

        try:
            fecha = datetime.fromisoformat(fecha_str)
        except Exception:
            return False, "Fecha inválida. Formato: YYYY-MM-DD HH:MM"

        # turno de 30 min
        hora_inicio = fecha.time()
        hora_fin = (fecha.replace(second=0, microsecond=0) + timedelta(minutes=30)).time()

        # si no tenés consultorio resuelto, usamos 1 para probar
        id_consultorio = 1

        ok = self.gestor.alta_turno(
            id_paciente=int(dni),
            matricula=int(matricula),
            id_consultorio=id_consultorio,
            fecha=fecha.date(),
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            observaciones=""
        )
        return (True, "Turno creado") if ok else (False, "No se pudo crear el turno")

    def cambiar_estado(self, dni, matricula, fecha_str, estado):
        """
        Tu gestor necesita id_turno para modificar.
        Buscamos el turno por (paciente, matrícula, fecha+hora_inicio) y actualizamos.
        """
        if not self.gestor.cargar_turnos_bd():
            return False, "No se pudieron cargar turnos"

        try:
            dt = datetime.fromisoformat(fecha_str)
        except Exception:
            return False, "Fecha inválida"

        fecha = dt.date()
        hora_inicio = dt.time()

        for t in self.gestor.get_turnos_bd():
            if (t.get("id_paciente") == int(dni)
                and t.get("matricula") == int(matricula)
                and str(t.get("fecha")) == str(fecha)
                and str(t.get("hora_inicio")) == str(hora_inicio)):
                id_turno = t["id_turno"]
                estado_bd = estado.capitalize()  # tu BD usa 'Programado', 'Atendido', etc.
                ok = self.gestor.modificar_turno_bd(id_turno, estado=estado_bd)
                return (True, "Estado actualizado") if ok else (False, "No se pudo cambiar estado")

        return False, "Turno no encontrado"

    def listar(self):
        self.gestor.cargar_turnos_bd()
        salida = []
        for t in self.gestor.get_turnos_bd():
            salida.append({
                "id_turno": t.get("id_turno"),
                "dni": t.get("id_paciente"),
                "mat": t.get("matricula"),
                "fecha": f"{t.get('fecha')} {t.get('hora_inicio')}",
                "estado": t.get("estado")
            })
        return salida
