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
        # ===== generar PDF de una receta existente (mejorado) =====
    def generar_pdf(self, id_receta: int, output_path: str) -> bool:
        """
        Genera un PDF prolijo estilo "receta electrónica" SIN dependencias raras.
        - Si hay logo.png o firma.png en frontend/assets, los usa.
        - Si algo falta, lo omite y sigue.
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm
            from reportlab.lib import colors
            from reportlab.graphics.barcode import qr as qrbar  # QR built-in
        except Exception:
            print("Falta reportlab: pip install reportlab")
            return False

        # 1) Traer datos
        if not self._connect():
            return False
        try:
            cab = self._one(
                """SELECT r.id_receta, r.fecha_emision, r.fecha_vencimiento,
                        p.nombre AS p_nom, p.apellido AS p_ape,
                        p.id_paciente,
                        m.nombre AS m_nom, m.apellido AS m_ape, m.matricula,
                        t.fecha, t.hora_inicio, t.hora_fin,
                        c.numero AS consultorio,
                        h.diagnostico AS diag 
                    FROM Receta r
                    JOIN Historial_clinico h ON h.id_historial = r.id_historial
                    JOIN Turno t ON t.id_turno = h.id_turno
                    JOIN Paciente p ON p.id_paciente = t.id_paciente
                    JOIN Medico m ON m.matricula = t.matricula
                    JOIN Consultorio c ON c.id_consultorio = t.id_consultorio
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

        # 2) PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        w, h = A4
        y = h - 2*cm

        # Rutas de assets opcionales
        ASSETS = os.path.join(BASE, "frontend", "assets")
        logo_path = os.path.join(ASSETS, "logo.png")
        firma_path = os.path.join(ASSETS, "firma.png")

        # Encabezado: Logo + título + Nº Receta + Fecha
        if os.path.exists(logo_path):
            try:
                c.drawImage(logo_path, 2*cm, y-1.5*cm, width=3*cm, height=1.5*cm, preserveAspectRatio=True, mask='auto')
            except:
                pass

        c.setFont("Helvetica-Bold", 14)
        c.drawString(6*cm, y, "RECETA MÉDICA")
        c.setFont("Helvetica", 10)
        c.drawRightString(w-2*cm, y, f"Nº Receta: {cab['id_receta']}")
        y -= 0.6*cm
        c.drawRightString(w-2*cm, y, f"Fecha: {str(cab['fecha_emision'])}")
        y -= 1.0*cm

        # Caja datos de paciente / médico
        c.setStrokeColor(colors.black)
        c.rect(2*cm, y-2.3*cm, w-4*cm, 2.3*cm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(2.2*cm, y-0.5*cm, "Paciente:")
        c.setFont("Helvetica", 11)
        c.drawString(4.2*cm, y-0.5*cm, f"{cab['p_nom']} {cab['p_ape']}  (ID: {cab['id_paciente']})")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(2.2*cm, y-1.2*cm, "Médico:")
        c.setFont("Helvetica", 11)
        c.drawString(4.2*cm, y-1.2*cm, f"Dr/a. {cab['m_nom']} {cab['m_ape']}  Matrícula: {cab['matricula']}")

        c.setFont("Helvetica", 10)
        c.drawString(2.2*cm, y-1.9*cm, f"Turno: {cab['fecha']} | {cab['hora_inicio']} - {cab['hora_fin']} | Consultorio {cab['consultorio']}")
        y -= 2.8*cm

        # Título Prescripción
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "Prescripción")
        y -= 0.4*cm
        c.line(2*cm, y, w-2*cm, y)
        y -= 0.4*cm

        # Encabezados tabla
        c.setFont("Helvetica-Bold", 10)
        col_x = [2*cm, 3.5*cm, 10.5*cm, 15.5*cm]  # Cant | Monodroga | Presentación | Dosis
        headers = ["Cant", "Monodroga", "Presentación", "Dosis/día"]
        for i, htxt in enumerate(headers):
            c.drawString(col_x[i], y, htxt)
        y -= 0.35*cm
        c.line(2*cm, y, w-2*cm, y)
        y -= 0.3*cm

        # Filas de medicamentos
        c.setFont("Helvetica", 10)
        for i, it in enumerate(det or [], 1):
            if y < 4*cm:  # salto de página simple
                c.showPage()
                c.setFont("Helvetica", 10)
                y = h - 2*cm

            c.drawString(col_x[0], y, str(it.get("cantidad", "")))
            c.drawString(col_x[1], y, f"{it.get('nombre','')}")
            c.drawString(col_x[2], y, f"{it.get('presentacion','')}")
            c.drawString(col_x[3], y, f"{it.get('dosis','')}")
            y -= 0.45*cm
            if it.get("indicaciones"):
                c.setFont("Helvetica-Oblique", 9)
                c.drawString(col_x[1], y, f"Indicaciones: {it['indicaciones']}")
                c.setFont("Helvetica", 10)
                y -= 0.4*cm

        y -= 0.2*cm
        c.line(2*cm, y, w-2*cm, y)
        y -= 0.6*cm

        # ----- Diagnóstico (caja + texto con wrap) -----
        c.setFont("Helvetica-Bold", 11)
        c.drawString(2*cm, y, "Diagnóstico:")
        y -= 0.5*cm

        box_x = 2*cm
        box_w = w - 4*cm
        box_h = 2.2*cm       # ajustá si querés más alto
        box_y = y - box_h
        c.rect(box_x, box_y, box_w, box_h, stroke=1, fill=0)

        # texto del diagnóstico (viene de h.diagnostico AS diag en la query)
        diag = (cab.get("diag") or "").strip()
        if diag:
            from reportlab.pdfbase.pdfmetrics import stringWidth
            c.setFont("Helvetica", 10)
            max_w = box_w - 0.6*cm
            tx_y = box_y + box_h - 0.7*cm
            line = ""
            for word in diag.split():
                test = (line + " " + word).strip()
                if stringWidth(test, "Helvetica", 10) <= max_w:
                    line = test
                else:
                    c.drawString(box_x + 0.3*cm, tx_y, line)
                    tx_y -= 0.45*cm
                    line = word
                    if tx_y < box_y + 0.5*cm:
                        break
            if line and tx_y >= box_y + 0.5*cm:
                c.drawString(box_x + 0.3*cm, tx_y, line)

        # dejamos el cursor debajo de la caja
        y = box_y - 0.6*cm

                # ===== Bloque inferior: QR (izq) + Firma (der), sin solaparse =====
        # Si no hay altura suficiente, salto de página
        if y < 6*cm:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = h - 2*cm

        block_top = y

        # ---- QR a la izquierda ----
        size = 3.2*cm
        qr_x = 2*cm
        qr_y = block_top - size  # default, por si falla el render

        try:
            from reportlab.graphics.shapes import Drawing
            from reportlab.graphics import renderPDF
            qr_text = f"RECETA:{cab['id_receta']}|PAC:{cab['p_nom']} {cab['p_ape']}|F:{cab['fecha_emision']}"
            qr = qrbar.QrCodeWidget(qr_text)
            bounds = qr.getBounds()
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            d = Drawing(size, size, transform=[size/width, 0, 0, size/height, 0, 0])
            d.add(qr)
            renderPDF.draw(d, c, qr_x, qr_y)
        except Exception:
            pass  # si falla el QR, seguimos

        # ---- Firma a la derecha ----
        sig_w = 5*cm
        sig_h = 2*cm
        sig_x = w - 2*cm - sig_w
        sig_y = block_top - 1.6*cm

        if os.path.exists(firma_path):
            try:
                c.drawImage(firma_path, sig_x, sig_y, width=sig_w, height=sig_h,
                            preserveAspectRatio=True, mask='auto')
            except Exception:
                c.line(sig_x, sig_y + 0.2*cm, sig_x + sig_w, sig_y + 0.2*cm)
        else:
            c.line(sig_x, sig_y + 0.2*cm, sig_x + sig_w, sig_y + 0.2*cm)

        c.setFont("Helvetica", 10)
        c.drawCentredString(sig_x + sig_w/2, sig_y - 0.4*cm,
                            f"Dr/a. {cab['m_nom']} {cab['m_ape']}  -  Matrícula {cab['matricula']}")

        # Ajusto cursor Y por debajo del bloque firma/QR
        y = min(qr_y, sig_y - 1.0*cm)


        # Pie con barras “fake” (solo texto) + leyenda
        y -= 3.0*cm
        c.line(2*cm, y, w-2*cm, y)
        y -= 0.5*cm
        c.setFont("Helvetica", 9)
        c.drawString(2*cm, y, f"Nº de receta: {cab['id_receta']}")
        c.drawRightString(w-2*cm, y, f"Paciente ID: {cab['id_paciente']}")
        y -= 0.5*cm
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(2*cm, y, "Documento generado por el Sistema de Gestión Médica. Uso profesional.")

        c.showPage()
        c.save()
        return True
