import logging
import sys
from loguru import logger
from pathlib import Path

"""
Configura o sistema de logs
Utiliza loguru para logs estruturados e rotacionados
"""


# Configurar logs
def setup_logger():
    # Remover handler padrão do loguru
    logger.remove()

    # Configurar formato dos logs
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # Log para console
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )

    # Log para arquivo
    log_file = Path("logs/app.log")
    log_file.parent.mkdir(exist_ok=True)

    logger.add(
        log_file,
        format=log_format,
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

    # Log de erros separado
    error_log_file = Path("logs/errors.log")
    logger.add(
        error_log_file,
        format=log_format,
        level="ERROR",
        rotation="5 MB",
        retention="60 days",
        compression="zip"
    )

    return logger


# Instanciar logger configurado
app_logger = setup_logger()


def log_api_request(method: str, path: str, status_code: int, duration: float):
    """Log de requisições da API"""
    level = "INFO" if status_code < 400 else "WARNING" if status_code < 500 else "ERROR"
    app_logger.log(level, f"API Request: {method} {path} - {status_code} ({duration:.3f}s)")


def log_database_operation(operation: str, table: str, duration: float):
    """Log de operações do banco de dados"""
    app_logger.info(f"Database: {operation} on {table} ({duration:.3f}s)")


def log_business_validation(validation_type: str, details: str):
    """Log de validações de negócio"""
    app_logger.info(f"Validation: {validation_type} - {details}")


def log_error(error: Exception, context: str = ""):
    """Log de erros"""
    app_logger.error(f"Error in {context}: {str(error)}")
    app_logger.exception(error)
