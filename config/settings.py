"""Configuración centralizada de la aplicación"""

# Base de datos
DATABASE_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "hospital_db"
}

# Aplicación
APP_NAME = "Sistema de Gestión Médica"
APP_VERSION = "1.0.0"
DEBUG = True

# Logs
LOG_FILE = "app.log"