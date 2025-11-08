#!/usr/bin/env python3
"""
File Selector Widget - Drag-and-drop image selector with preview
"""

import os
from pathlib import Path
from typing import Optional, Callable
import customtkinter as ctk
from tkinter import filedialog


class FileSelector(ctk.CTkFrame):
    """Advanced file selector with drag-and-drop support and preview."""
    
    def __init__(self, parent, on_file_selected: Optional[Callable] = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_file_selected = on_file_selected
        self.selected_file: Optional[str] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the file selector UI."""
        title = ctk.CTkLabel(
            self,
            text="📁 Boot Image Selection",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=(10, 5), padx=15, anchor="w")
        
        self.drop_frame = ctk.CTkFrame(self, height=120, corner_radius=10)
        self.drop_frame.pack(fill="x", padx=15, pady=10)
        
        drop_icon = ctk.CTkLabel(
            self.drop_frame,
            text="📤",
            font=("Helvetica", 48)
        )
        drop_icon.pack(pady=(15, 5))
        
        drop_text = ctk.CTkLabel(
            self.drop_frame,
            text="Drag & Drop boot.img or recovery.img here\nor click Browse button below",
            font=("Helvetica", 12)
        )
        drop_text.pack(pady=(0, 15))
        
        self.file_info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_info_frame.pack(fill="x", padx=15, pady=5)
        
        self.filename_label = ctk.CTkLabel(
            self.file_info_frame,
            text="No file selected",
            font=("Helvetica", 11),
            text_color="gray"
        )
        self.filename_label.pack(side="left")
        
        self.filesize_label = ctk.CTkLabel(
            self.file_info_frame,
            text="",
            font=("Helvetica", 10),
            text_color="gray"
        )
        self.filesize_label.pack(side="right")
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        browse_btn = ctk.CTkButton(
            button_frame,
            text="Browse Files",
            command=self.browse_file,
            width=120,
            height=32
        )
        browse_btn.pack(side="left", padx=(0, 10))
        
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_selection,
            width=80,
            height=32,
            fg_color="#8B0000",
            hover_color="#A52A2A"
        )
        self.clear_btn.pack(side="left")
        self.clear_btn.configure(state="disabled")
    
    def browse_file(self):
        """Open file browser dialog."""
        file_types = [
            ("Image Files", "*.img *.tar *.gz *.lz4 *.zip"),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Boot/Recovery Image",
            filetypes=file_types
        )
        
        if filename:
            self.set_file(filename)
    
    def set_file(self, filepath: str):
        """Set the selected file and update UI."""
        if not os.path.exists(filepath):
            return
        
        self.selected_file = filepath
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        
        filesize_str = self._format_filesize(filesize)
        
        self.filename_label.configure(
            text=f"✓ {filename}",
            text_color="#4CAF50"
        )
        self.filesize_label.configure(
            text=filesize_str,
            text_color="#4CAF50"
        )
        
        self.clear_btn.configure(state="normal")
        
        if self.on_file_selected:
            self.on_file_selected(filepath)
    
    def clear_selection(self):
        """Clear the selected file."""
        self.selected_file = None
        self.filename_label.configure(
            text="No file selected",
            text_color="gray"
        )
        self.filesize_label.configure(text="")
        self.clear_btn.configure(state="disabled")
    
    def get_selected_file(self) -> Optional[str]:
        """Get the currently selected file path."""
        return self.selected_file
    
    def _format_filesize(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
