# TPDAO - Sistema de Gestión Médica

## Instalación

Instalar dependencias:
```bash
pip install mysql-connector-python
pip install reportlab
pip install matplotlib
pip install tkcalendar
pip install python-dotenv
```

O instalar todas de una vez:
```bash
pip install mysql-connector-python reportlab matplotlib tkcalendar python-dotenv
```

## Configuración de Base de Datos

1. Configurar credenciales en `data/database.py`:
   - Si **no tienes contraseña**: `self.password = ""`
   - Si **tienes contraseña**: `self.password = "tu_contraseña"`

## Crear la base de datos

1. Ejecutar el script `data/hospital_db_tpdao_create.sql`
2. Ejecutar el script `data/hospital_db_tpdao_inserts.sql`

## Ejecutar la aplicación

```bash
python -m frontend.app
```

## Características Principales

### Creación de Médicos
Al crear un nuevo médico, puedes:
- ✅ Asignar especialidades
- ✅ Programar agenda (días y horarios)
- ✅ Generar automáticamente turnos de 30 minutos para los próximos 30 días

**Nota:** Ya no es necesario ejecutar `generar_turnos.py` manualmente. Los turnos se generan automáticamente al crear/modificar la agenda de un médico.

## Estructura del proyecto

```
TPDAO/
├── entidades/          # Clases de entidades (Paciente, Medico, etc.)
├── gestores/           # Lógica de negocio ABMC
├── frontend/           # Interfaz gráfica Tkinter
├── data/               # Scripts SQL y clase Database
├── reports/            # Generación de reportes
└── enums.py           # Enumeraciones del sistema
```

## Dependencias del proyecto

- **mysql-connector-python**: Conexión a MySQL
- **reportlab**: Generación de PDFs (recetas)
- **matplotlib**: Gráficos estadísticos
- **tkcalendar**: Selector de fechas en la UI
- **python-dotenv**: Variables de entorno para notificaciones