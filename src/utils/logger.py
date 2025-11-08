#!/usr/bin/env python3
"""
Logger - Application logging system

Handles logging of application events and errors.
"""

import os
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Application logger with file and console output."""
    
    def __init__(self, log_dir: str = "logs", log_level: int = logging.INFO):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"dtgen_{timestamp}.log"
        
        self.logger = logging.getLogger("DTGenerator")
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.WARNING)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        self.log_file = log_file
        self.log(f"Logger initialized. Log file: {log_file}")
    
    def log(self, message: str, level: str = "info"):
        """
        Log a message.
        
        Args:
            message: Message to log
            level: Log level (debug, info, warning, error, critical)
        """
        level = level.lower()
        
        if level == "debug":
            self.logger.debug(message)
        elif level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "critical":
            self.logger.critical(message)
        else:
            self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)
    
    def get_log_file_path(self) -> str:
        """Get the path to the current log file."""
        return str(self.log_file)
    
    def clean_old_logs(self, days: int = 7):
        """
        Remove log files older than specified days.
        
        Args:
            days: Number of days to keep logs
        """
        try:
            current_time = datetime.now().timestamp()
            cutoff_time = current_time - (days * 24 * 60 * 60)
            
            for log_file in self.log_dir.glob("dtgen_*.log"):
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
                    self.logger.info(f"Removed old log file: {log_file}")
        
        except Exception as e:
            self.logger.error(f"Error cleaning old logs: {e}")
