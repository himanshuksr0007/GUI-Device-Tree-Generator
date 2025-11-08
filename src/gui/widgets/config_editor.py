#!/usr/bin/env python3
"""
Config Editor - Interactive device tree configuration editor
"""

import customtkinter as ctk
from typing import Dict, Any, Optional


class ConfigEditor(ctk.CTkFrame):
    """Interactive editor for device tree configuration."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.config_data: Dict[str, Any] = {}
        self.widgets: Dict[str, ctk.CTkEntry] = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup config editor UI."""
        title = ctk.CTkLabel(
            self,
            text="⚙️ Device Configuration",
            font=("Helvetica", 14, "bold")
        )
        title.pack(pady=(10, 10), padx=15, anchor="w")
        
        scrollable_frame = ctk.CTkScrollableFrame(self, height=300)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.content_frame = scrollable_frame
        
        config_fields = [
            ("Device Codename", "device_codename", "Device code name (e.g., oneplus8pro)"),
            ("Manufacturer", "manufacturer", "Device manufacturer (e.g., OnePlus)"),
            ("Model", "model", "Device model name"),
            ("Architecture", "architecture", "CPU architecture (arm, arm64, x86, x86_64)"),
            ("Platform", "platform", "Device platform (e.g., qcom, mt6765)"),
            ("Kernel Version", "kernel_version", "Kernel version string"),
            ("Android Version", "android_version", "Android version (e.g., 11, 12, 13)"),
        ]
        
        for label_text, key, placeholder in config_fields:
            self._add_field(label_text, key, placeholder)
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Apply Changes",
            command=self._on_save,
            width=120,
            height=32,
            fg_color="#4CAF50",
            hover_color="#45A049"
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self._on_reset,
            width=80,
            height=32
        )
        reset_btn.pack(side="left")
    
    def _add_field(self, label: str, key: str, placeholder: str):
        """Add a configuration field."""
        field_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)
        
        label_widget = ctk.CTkLabel(
            field_frame,
            text=label + ":",
            font=("Helvetica", 11),
            width=150,
            anchor="w"
        )
        label_widget.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(
            field_frame,
            placeholder_text=placeholder,
            font=("Helvetica", 10)
        )
        entry.pack(side="left", fill="x", expand=True)
        
        self.widgets[key] = entry
    
    def load_config(self, config: Dict[str, Any]):
        """Load configuration data into editor."""
        self.config_data = config.copy()
        
        for key, value in config.items():
            if key in self.widgets:
                self.widgets[key].delete(0, "end")
                self.widgets[key].insert(0, str(value))
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration from editor."""
        config = {}
        for key, widget in self.widgets.items():
            value = widget.get().strip()
            if value:
                config[key] = value
        return config
    
    def _on_save(self):
        """Handle save button click."""
        self.config_data = self.get_config()
    
    def _on_reset(self):
        """Handle reset button click."""
        for widget in self.widgets.values():
            widget.delete(0, "end")
