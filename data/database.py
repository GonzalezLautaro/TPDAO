from typing import Optional
import mysql.connector
from mysql.connector import Error


class Database:
    """Singleton para conexión a base de datos MySQL"""
    
    __instancia = None
    __inicializado = False
    
    def __new__(cls):
        """Implementa el patrón Singleton"""
        if cls.__instancia is None:
            cls.__instancia = super().__new__(cls)
        return cls.__instancia
    
    def __init__(self):
        """Inicializa solo una vez"""
        if not Database.__inicializado:
            self.__connection = None
            self.__host = "127.0.0.1"
            self.__port = 3306
            self.__user = "root"
            self.__password = "root"
            self.__database = "hospital_db"
            Database.__inicializado = True
    
    def conectar(self, config_str: str) -> bool:
        """
        Conecta a la base de datos
        config_str: "host:puerto/nombre_bd"
        """
        try:
            partes = config_str.split("/")
            host_puerto = partes[0].split(":")
            self.__host = host_puerto[0]
            self.__port = int(host_puerto[1]) if len(host_puerto) > 1 else 3306
            self.__database = partes[1] if len(partes) > 1 else "hospital_db"
            
            self.__connection = mysql.connector.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                database=self.__database
            )
            # ✅ CAMBIAR: ✓ → [OK]
            print(f"[OK] Conectado a {self.__database}")
            return True
        except Error as e:
            # ✅ CAMBIAR: ✗ → [ERROR]
            print(f"[ERROR] Error de conexión: {e}")
            return False
    
    def obtener_registro(self, query: str, params: tuple = None):
        """Obtiene un registro"""
        try:
            cursor = self.__connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Error as e:
            # ✅ CAMBIAR: ✗ → [ERROR]
            print(f"[ERROR] {e}")
            return None
    
    def obtener_registros(self, query: str, params: tuple = None) -> list:
        """Obtiene registros"""
        try:
            cursor = self.__connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Error as e:
            # ✅ CAMBIAR: ✗ → [ERROR]
            print(f"[ERROR] {e}")
            return []
    
    def ejecutar_parametrizado(self, query: str, params: tuple) -> bool:
        """Ejecuta una consulta parametrizada (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, params)
            self.__connection.commit()
            cursor.close()
            return True
        except Error as e:
            # ✅ CAMBIAR: ✗ → [ERROR]
            print(f"[ERROR] {e}")
            return False
    
    def desconectar(self) -> None:
        """Cierra la conexión"""
        if self.__connection and self.__connection.is_connected():
            self.__connection.close()
            # ✅ CAMBIAR: ✓ → [OK]
            print("[OK] Desconectado de la base de datos")
    
    def __repr__(self) -> str:
        # ✅ CAMBIAR: ✓ y ✗ → [OK] y [OFFLINE]
        estado = "[OK] Conectado" if self.__connection else "[OFFLINE] Desconectado"
        return f"Database({self.__database}, {estado})"