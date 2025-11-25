from datetime import date
import sys, os

# Asegurá que TPDAO esté en el path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

# <<< IMPORT CORRECTO SEGÚN TU ARCHIVO >>>
# Si tu archivo se llama 'gestorpaciente.py':
from gestores.gestor_paciente import GestorPaciente
# Si en tu repo el archivo se llama 'gestopaciente.py' (sin 'r'), cambiá la línea de arriba por:
# from gestores.gestopaciente import GestorPaciente


class PacientesController:
    def __init__(self):
        self.gestor = GestorPaciente()

    def crear(self, nro, nombre, apellido, tel, nacimiento, direccion):
        if not nro or not nombre or not apellido:
            return False, "Faltan datos (id, nombre, apellido)"
        try:
            fecha_nac = date.fromisoformat(nacimiento)
        except Exception:
            return False, "Fecha de nacimiento inválida (YYYY-MM-DD)"
        ok = self.gestor.alta_paciente(int(nro), nombre, apellido, tel, fecha_nac, direccion)
        return (True, "Paciente creado") if ok else (False, "No se pudo crear")

    def listar(self):
        res = []
        for p in self.gestor.get_pacientes():
            res.append({
                "id": p.get_nro_paciente(),
                "nombre": p.get_nombre(),
                "apellido": p.get_apellido(),
                "telefono": p.get_telefono(),
                "direccion": p.get_direccion(),
                "nacimiento": str(p.get_fecha_nacimiento())
            })
        return res
