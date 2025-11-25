from datetime import date
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gestores.gestor_medico import GestorMedico


class MedicosController:
    def __init__(self):
        self.gestor = GestorMedico()

    def crear(self, matricula, nombre, apellido, tel, email, fecha_alta):
        try:
            fecha = date.fromisoformat(fecha_alta)
        except Exception:
            return False, "Fecha inválida (YYYY-MM-DD)"
        ok = self.gestor.alta_medico(int(matricula), nombre, apellido, tel, email, fecha)
        return (True, "Médico creado") if ok else (False, "No se pudo crear médico")

    def listar(self):
        res = []
        for m in self.gestor.get_medicos():
            res.append({
                "matricula": m.get_matricula(),
                "nombre": m.get_nombre(),
                "apellido": m.get_apellido(),
                "telefono": m.get_telefono(),
                "email": m.get_email(),
                "fecha_alta": str(m.get_fecha_alta())
            })
        return res
