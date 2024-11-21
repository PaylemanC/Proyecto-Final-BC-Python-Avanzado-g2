"""
This module contains variables that should be imported
and used to configure the logger.
"""
import sys
from config import ENVIRONMENT


log_output = sys.stdout
log_format = "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}"
log_level = "INFO" if ENVIRONMENT == "PROD" else "DEBUG"
