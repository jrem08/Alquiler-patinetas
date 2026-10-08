"""Configuracion y conexion a MySQL."""

import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> mysql.connector.MySQLConnection:
    """Abre una conexion usando las variables definidas en .env."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "alquiler_patinetas"),
        user=os.getenv("DB_USER", "alquiler_api"),
        password=os.getenv("DB_PASSWORD", ""),
        connection_timeout=5,
    )