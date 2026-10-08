CREATE USER IF NOT EXISTS 'alquiler_api'@'localhost'
    IDENTIFIED BY 'CAMBIA_ESTA_CLAVE';

GRANT SELECT, INSERT, UPDATE, DELETE
    ON alquiler_patinetas.*
    TO 'alquiler_api'@'localhost';

FLUSH PRIVILEGES;