"""
Script principal - Sistema de Gestión Médica
Interfaz gráfica con Tkinter
"""

from data.database import Database


def main():
    """Función principal que inicia la aplicación"""
    
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN MÉDICA")
    print("=" * 60)
    
    # Obtener instancia Singleton de Database
    db = Database()
    
    if db.conectar("127.0.0.1:3306/hospital_db"):
        print(f"[OK] {db}")
        print("[OK] Conectado a la base de datos")
        
        # Importar y ejecutar la interfaz gráfica
        print("\n[INFO] Iniciando interfaz gráfica...\n")
        
        try:
            from frontend.main_window import run_app
            run_app()
        except ImportError as e:
            print(f"[ERROR] Error al importar frontend: {e}")
            print("[ERROR] Asegúrate de que la carpeta 'frontend' existe y contiene 'main_window.py'")
        except Exception as e:
            print(f"[ERROR] Error al ejecutar la aplicación: {e}")
        finally:
            db.desconectar()
            print("[OK] Desconectado de la base de datos")
    else:
        print("[ERROR] No se pudo conectar a la base de datos")

if __name__ == "__main__":
    main()