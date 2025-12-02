# TPDAO/frontend/controllers/recetas_controller.py
from typing import Optional, List, Dict
import os, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database  # usa TU clase, pero con cursor directo

class RecetasController:
    def __init__(self):
        self.db = Database()

    def _connect(self) -> bool:
        # mismo DSN que venís usando; ajustá si lo cambiaste
        return self.db.conectar("127.0.0.1:3306/hospital_db")

    # ----- helpers internos SIN depender de ejecutar_consulta/obtener_* -----
    def _one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        cur = self.db.connection.cursor(dictionary=True)
        cur.execute(query, params)
        row = cur.fetchone()
        cur.close()
        return row

    def _all(self, query: str, params: tuple = ()) -> List[Dict]:
        cur = self.db.connection.cursor(dictionary=True)
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        return rows

    def id_receta_de_turno(self, id_turno: int) -> Optional[int]:
        if not self._connect():
            return None
        try:
            row = self._one(
                """SELECT r.id_receta
                   FROM Receta r
                   JOIN Historial_clinico h ON h.id_historial = r.id_historial
                   WHERE h.id_turno = %s
                   ORDER BY r.id_receta DESC
                   LIMIT 1""",
                (id_turno,)
            )
            return row["id_receta"] if row else None
        finally:
            self.db.desconectar()

    # ===== generar PDF de una receta existente =====
    def generar_pdf(self, id_receta: int, output_path: str) -> bool:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm
        except Exception:
            print("Falta reportlab: pip install reportlab")
            return False

        if not self._connect():
            return False

        try:
            cab = self._one(
                """SELECT r.id_receta, r.fecha_emision, r.fecha_vencimiento,
                          p.nombre AS p_nom, p.apellido AS p_ape,
                          m.nombre AS m_nom, m.apellido AS m_ape
                   FROM Receta r
                   JOIN Historial_clinico h ON h.id_historial = r.id_historial
                   JOIN Turno t ON t.id_turno = h.id_turno
                   JOIN Paciente p ON p.id_paciente = t.id_paciente
                   JOIN Medico m ON m.matricula = t.matricula
                   WHERE r.id_receta = %s""",
                (id_receta,)
            )
            det = self._all(
                """SELECT d.cantidad, d.dosis, d.indicaciones,
                          med.nombre, med.presentacion
                   FROM Detalle_receta d
                   JOIN Medicamento med ON med.id_medicamento = d.id_medicamento
                   WHERE d.id_receta = %s""",
                (id_receta,)
            )
        finally:
            self.db.desconectar()

        if not cab:
            return False

        # Render PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        w, h = A4
        y = h - 2*cm

        c.setFont("Helvetica-Bold", 14)
        c.drawString(2*cm, y, "RECETA MÉDICA"); y -= 1.2*cm

        c.setFont("Helvetica", 11)
        c.drawString(2*cm, y, f"Paciente: {cab['p_nom']} {cab['p_ape']}"); y -= 0.6*cm
        c.drawString(2*cm, y, f"Médico: {cab['m_nom']} {cab['m_ape']}"); y -= 0.6*cm
        c.drawString(2*cm, y, f"Emisión: {cab['fecha_emision']}   Vto: {cab['fecha_vencimiento']}"); y -= 1.0*cm

        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "Detalle:"); y -= 0.8*cm
        c.setFont("Helvetica", 11)

        for i, it in enumerate(det or [], 1):
            linea = f"{i}. {it['nombre']} ({it.get('presentacion','')})  x{it['cantidad']}  - Dosis: {it.get('dosis','')}"
            c.drawString(2*cm, y, linea); y -= 0.5*cm
            if it.get('indicaciones'):
                c.drawString(2.5*cm, y, f"Indicaciones: {it['indicaciones']}"); y -= 0.5*cm
            if y < 3*cm:
                c.showPage(); y = h - 2*cm; c.setFont("Helvetica", 11)

        c.showPage()
        c.save()
        return True
