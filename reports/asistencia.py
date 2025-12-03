# TPDAO/reports/asistencia.py
"""
Gráfico de asistencia vs inasistencia desde la BD.
Ignora los turnos en estado 'Libre' (y cualquier otro estado no relevante).
"""

import os
from typing import Optional, Tuple

import mysql.connector
import matplotlib.pyplot as plt


def _contar_asistencias(
    host: str = "127.0.0.1",
    user: str = "root",
    password: str = "",
    database: str = "hospital_db",
    port: int = 3306,
) -> Tuple[int, int]:
    """
    Devuelve (asistieron, no_asistieron) leyendo de la tabla Turno.
    Cuenta:
      - Asistieron: estado = 'Atendido'
      - No asistieron: estado = 'Inasistencia'
    Ignora 'Libre' (y cualquier otro estado).
    """
    conn = mysql.connector.connect(
        host=host, user=user, password=password, database=database, port=port
    )
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT estado, COUNT(*) 
            FROM Turno
            WHERE estado IN ('Atendido','Inasistencia')
            GROUP BY estado
        """)
        asist, no_asist = 0, 0
        for estado, cant in cur.fetchall():
            if estado == "Atendido":
                asist = int(cant)
            elif estado == "Inasistencia":
                no_asist = int(cant)
        return asist, no_asist
    finally:
        conn.close()


def grafico_asistencia_bd(
    ruta_salida: str,
    *,
    host: str = "127.0.0.1",
    user: str = "root",
    password: str = "",
    database: str = "hospital_db",
    port: int = 3306,
    tipo: str = "pie",   # "pie" o "bar"
) -> Optional[str]:
    """
    Genera el gráfico en 'ruta_salida' y devuelve esa ruta.
    Si no hay datos (0 y 0), igual genera una imagen con el aviso.
    """
    # 1) Datos
    asist, no_asist = _contar_asistencias(
        host=host, user=user, password=password, database=database, port=port
    )

    # 2) Preparar carpeta
    parent = os.path.dirname(ruta_salida)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    # 3) Graficar
    fig, ax = plt.subplots(figsize=(6, 6))

    if asist == 0 and no_asist == 0:
        ax.text(0.5, 0.5, "Sin datos de asistencia", ha="center", va="center", fontsize=12)
        ax.axis("off")
    else:
        labels = ["Asistieron", "No asistieron"]
        values = [asist, no_asist]

        if tipo == "bar":
            bars = ax.bar(labels, values)
            for i, v in enumerate(values):
                ax.text(i, v + max(values) * 0.02, str(v), ha="center", fontsize=10)
            ax.set_ylabel("Cantidad")
        else:
            # Pie con leyenda abajo a la derecha
            colors = ["#4CAF50", "#F44336"]
            wedges, texts, autotexts = ax.pie(
                values, labels=None, autopct="%1.1f%%", startangle=90,
                colors=colors, pctdistance=0.75
            )
            ax.axis("equal")
            ax.legend(
                wedges, labels, title="Leyenda",
                loc="lower right", bbox_to_anchor=(1.0, 0.0)
            )
            # números más legibles
            for t in autotexts:
                t.set_fontsize(10)
                t.set_color("black")

        ax.set_title("Asistencia a turnos (solo Atendido vs Inasistencia)")

    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close(fig)
    return ruta_salida
