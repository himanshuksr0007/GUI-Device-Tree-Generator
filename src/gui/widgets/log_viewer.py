#!/usr/bin/env python3
"""
Log Viewer - Syntax-highlighted log display with filtering
"""

import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from typing import Literal


class LogViewer(ctk.CTkFrame):
    """Advanced log viewer with syntax highlighting and filtering."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.log_levels = ["ALL", "INFO", "WARNING", "ERROR", "DEBUG"]
        self.current_filter = "ALL"
        
        self._setup_ui()
        self._configure_tags()
    
    def _setup_ui(self):
        """Setup log viewer UI."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title = ctk.CTkLabel(
            header_frame,
            text="📋 Generation Log",
            font=("Helvetica", 14, "bold")
        )
        title.pack(side="left")
        
        filter_label = ctk.CTkLabel(
            header_frame,
            text="Filter:",
            font=("Helvetica", 10)
        )
        filter_label.pack(side="right", padx=(0, 5))
        
        self.filter_menu = ctk.CTkOptionMenu(
            header_frame,
            values=self.log_levels,
            command=self._on_filter_changed,
            width=100
        )
        self.filter_menu.pack(side="right")
        self.filter_menu.set("ALL")
        
        clear_btn = ctk.CTkButton(
            header_frame,
            text="Clear",
            command=self.clear,
            width=60,
            height=25
        )
        clear_btn.pack(side="right", padx=(0, 10))
        
        self.text_widget = ctk.CTkTextbox(
            self,
            font=("Consolas", 10),
            wrap="word"
        )
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def _configure_tags(self):
        """Configure text tags for syntax highlighting."""
        self.text_widget._textbox.tag_config("INFO", foreground="#2196F3")
        self.text_widget._textbox.tag_config("WARNING", foreground="#FF9800")
        self.text_widget._textbox.tag_config("ERROR", foreground="#F44336")
        self.text_widget._textbox.tag_config("SUCCESS", foreground="#4CAF50")
        self.text_widget._textbox.tag_config("DEBUG", foreground="#9E9E9E")
        self.text_widget._textbox.tag_config("TIMESTAMP", foreground="#607D8B")
    
    def log(self, message: str, level: Literal["INFO", "WARNING", "ERROR", "SUCCESS", "DEBUG"] = "INFO"):
        """Add a log message with specified level."""
        if self.current_filter != "ALL" and self.current_filter != level:
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.text_widget.configure(state="normal")
        
        start_pos = self.text_widget.index("end-1c")
        self.text_widget.insert("end", f"[{timestamp}] ", "TIMESTAMP")
        self.text_widget.insert("end", f"[{level}] ", level)
        self.text_widget.insert("end", f"{message}\n")
        
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")
    
    def info(self, message: str):
        """Log info message."""
        self.log(message, "INFO")
    
    def warning(self, message: str):
        """Log warning message."""
        self.log(message, "WARNING")
    
    def error(self, message: str):
        """Log error message."""
        self.log(message, "ERROR")
    
    def success(self, message: str):
        """Log success message."""
        self.log(message, "SUCCESS")
    
    def debug(self, message: str):
        """Log debug message."""
        self.log(message, "DEBUG")
    
    def clear(self):
        """Clear all log messages."""
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.configure(state="disabled")
    
    def _on_filter_changed(self, value: str):
        """Handle filter change."""
        self.current_filter = value
