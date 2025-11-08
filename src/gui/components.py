#!/usr/bin/env python3
"""
Reusable GUI Components

This module contains reusable UI components for the application.
"""

import customtkinter as ctk
from typing import Callable, Optional


class StatusCard(ctk.CTkFrame):
    """A card widget for displaying status information."""
    
    def __init__(self, parent, title: str, icon: str = "", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title_label = ctk.CTkLabel(
            self,
            text=f"{icon} {title}" if icon else title,
            font=("Helvetica", 14, "bold")
        )
        self.title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.value_label = ctk.CTkLabel(
            self,
            text="--",
            font=("Helvetica", 24, "bold")
        )
        self.value_label.pack(padx=15, pady=5)
        
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="",
            font=("Helvetica", 10),
            text_color="gray"
        )
        self.subtitle_label.pack(padx=15, pady=(0, 10))
    
    def update_value(self, value: str, subtitle: str = ""):
        """Update the card value and subtitle."""
        self.value_label.configure(text=value)
        if subtitle:
            self.subtitle_label.configure(text=subtitle)


class ProgressStep(ctk.CTkFrame):
    """A widget for displaying progress steps."""
    
    def __init__(self, parent, step_number: int, title: str, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.step_number = step_number
        self.is_complete = False
        self.is_active = False
        
        self.circle = ctk.CTkLabel(
            self,
            text=str(step_number),
            width=40,
            height=40,
            font=("Helvetica", 14, "bold"),
            fg_color="gray",
            corner_radius=20
        )
        self.circle.pack(side="left", padx=(0, 10))
        
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Helvetica", 12)
        )
        self.title_label.pack(side="left")
    
    def set_active(self):
        """Mark step as active."""
        self.is_active = True
        self.circle.configure(fg_color="#2196F3")
    
    def set_complete(self):
        """Mark step as complete."""
        self.is_complete = True
        self.is_active = False
        self.circle.configure(fg_color="#4CAF50", text="✓")
    
    def set_error(self):
        """Mark step as error."""
        self.is_complete = False
        self.is_active = False
        self.circle.configure(fg_color="#F44336", text="✗")
    
    def reset(self):
        """Reset step to default state."""
        self.is_complete = False
        self.is_active = False
        self.circle.configure(fg_color="gray", text=str(self.step_number))


class InfoPanel(ctk.CTkFrame):
    """A panel for displaying information with key-value pairs."""
    
    def __init__(self, parent, title: str, **kwargs):
        super().__init__(parent, **kwargs)
        
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(anchor="w", padx=15, pady=(10, 10))
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        self.items = {}
    
    def add_item(self, key: str, value: str):
        """Add a key-value pair to the panel."""
        row = len(self.items)
        
        key_label = ctk.CTkLabel(
            self.content_frame,
            text=f"{key}:",
            font=("Helvetica", 11, "bold")
        )
        key_label.grid(row=row, column=0, sticky="w", pady=2)
        
        value_label = ctk.CTkLabel(
            self.content_frame,
            text=value,
            font=("Helvetica", 11)
        )
        value_label.grid(row=row, column=1, sticky="w", padx=(10, 0), pady=2)
        
        self.items[key] = value_label
    
    def update_item(self, key: str, value: str):
        """Update the value of an existing item."""
        if key in self.items:
            self.items[key].configure(text=value)
    
    def clear(self):
        """Clear all items from the panel."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.items.clear()
