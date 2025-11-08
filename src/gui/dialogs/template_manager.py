#!/usr/bin/env python3
"""
Template Manager - Manage ROM target templates
"""

import customtkinter as ctk


class TemplateManager(ctk.CTkToplevel):
    """Template manager dialog for ROM targets."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Template Manager")
        self.geometry("600x500")
        
        self._setup_ui()
        
        self.transient(parent)
        self.grab_set()
    
    def _setup_ui(self):
        """Setup template manager UI."""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_frame,
            text="📄 ROM Templates",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=(0, 20))
        
        info = ctk.CTkLabel(
            main_frame,
            text="Manage device tree templates for different ROM targets.",
            font=("Helvetica", 11)
        )
        info.pack(pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Feature coming in v1.1!", font=("Helvetica", 12)).pack(pady=20)
        
        ctk.CTkButton(
            main_frame,
            text="Close",
            command=self.destroy,
            width=100
        ).pack(side="bottom", pady=(20, 0))
