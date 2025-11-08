#!/usr/bin/env python3
"""
Settings Dialog - Application configuration settings
"""

import customtkinter as ctk
from typing import Dict, Any


class SettingsDialog(ctk.CTkToplevel):
    """Settings configuration dialog."""
    
    def __init__(self, parent, current_settings: Dict[str, Any] = None):
        super().__init__(parent)
        
        self.title("Settings")
        self.geometry("500x600")
        self.resizable(False, False)
        
        self.settings = current_settings or self._get_default_settings()
        self.result = None
        
        self._setup_ui()
        
        self.transient(parent)
        self.grab_set()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            'theme': 'dark',
            'auto_validate': True,
            'init_git': True,
            'verbose_logging': False,
            'default_output_dir': './output',
            'auto_open_output': True
        }
    
    def _setup_ui(self):
        """Setup settings dialog UI."""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_frame,
            text="⚙️ Application Settings",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=(0, 20))
        
        self.theme_var = ctk.StringVar(value=self.settings.get('theme', 'dark'))
        self.auto_validate_var = ctk.BooleanVar(value=self.settings.get('auto_validate', True))
        self.init_git_var = ctk.BooleanVar(value=self.settings.get('init_git', True))
        self.verbose_var = ctk.BooleanVar(value=self.settings.get('verbose_logging', False))
        self.auto_open_var = ctk.BooleanVar(value=self.settings.get('auto_open_output', True))
        
        ctk.CTkLabel(main_frame, text="Theme:", font=("Helvetica", 12)).pack(anchor="w", pady=(5, 2))
        ctk.CTkOptionMenu(
            main_frame,
            values=["Dark", "Light"],
            variable=self.theme_var
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkCheckBox(
            main_frame,
            text="Auto-validate generated device trees",
            variable=self.auto_validate_var
        ).pack(anchor="w", pady=5)
        
        ctk.CTkCheckBox(
            main_frame,
            text="Initialize Git repository by default",
            variable=self.init_git_var
        ).pack(anchor="w", pady=5)
        
        ctk.CTkCheckBox(
            main_frame,
            text="Enable verbose logging",
            variable=self.verbose_var
        ).pack(anchor="w", pady=5)
        
        ctk.CTkCheckBox(
            main_frame,
            text="Auto-open output directory after generation",
            variable=self.auto_open_var
        ).pack(anchor="w", pady=5)
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            command=self._on_save,
            width=100
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=100
        ).pack(side="right")
    
    def _on_save(self):
        """Save settings and close dialog."""
        self.result = {
            'theme': self.theme_var.get().lower(),
            'auto_validate': self.auto_validate_var.get(),
            'init_git': self.init_git_var.get(),
            'verbose_logging': self.verbose_var.get(),
            'auto_open_output': self.auto_open_var.get()
        }
        self.destroy()
