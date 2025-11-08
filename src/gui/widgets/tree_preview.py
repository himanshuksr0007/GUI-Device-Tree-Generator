#!/usr/bin/env python3
"""
Tree Preview - Generated files tree view with file content preview
"""

import os
from pathlib import Path
from typing import Optional
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk


class TreePreview(ctk.CTkFrame):
    """Tree view for browsing generated device tree files."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.current_path: Optional[str] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup tree preview UI."""
        title = ctk.CTkLabel(
            self,
            text="📂 Generated Files",
            font=("Helvetica", 14, "bold")
        )
        title.pack(pady=(10, 5), padx=10, anchor="w")
        
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("#0", text="File Structure", anchor="w")
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.open_btn = ctk.CTkButton(
            action_frame,
            text="Open in File Manager",
            command=self._open_in_file_manager,
            width=150,
            height=28
        )
        self.open_btn.pack(side="left", padx=(0, 10))
        self.open_btn.configure(state="disabled")
        
        self.refresh_btn = ctk.CTkButton(
            action_frame,
            text="Refresh",
            command=self.refresh,
            width=80,
            height=28
        )
        self.refresh_btn.pack(side="left")
        self.refresh_btn.configure(state="disabled")
    
    def load_directory(self, path: str):
        """Load directory tree."""
        self.current_path = path
        self.tree.delete(*self.tree.get_children())
        
        if not os.path.exists(path):
            return
        
        root_node = self.tree.insert("", "end", text=os.path.basename(path), open=True)
        self._populate_tree(root_node, path)
        
        self.open_btn.configure(state="normal")
        self.refresh_btn.configure(state="normal")
    
    def _populate_tree(self, parent, path: str):
        """Recursively populate tree with directory contents."""
        try:
            items = sorted(os.listdir(path))
            
            dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
            files = [item for item in items if os.path.isfile(os.path.join(path, item))]
            
            for dir_name in dirs:
                dir_path = os.path.join(path, dir_name)
                if not dir_name.startswith('.'):
                    node = self.tree.insert(parent, "end", text=f"📁 {dir_name}", open=False)
                    self._populate_tree(node, dir_path)
            
            for file_name in files:
                if not file_name.startswith('.'):
                    icon = self._get_file_icon(file_name)
                    self.tree.insert(parent, "end", text=f"{icon} {file_name}")
        
        except PermissionError:
            pass
    
    def _get_file_icon(self, filename: str) -> str:
        """Get appropriate icon for file type."""
        ext = Path(filename).suffix.lower()
        
        if ext in ['.mk', '.bp']:
            return "🔧"
        elif ext in ['.sh', '.bat']:
            return "📦"
        elif ext in ['.xml', '.json']:
            return "📄"
        elif ext == '.fstab':
            return "📊"
        elif ext == '.prop':
            return "⚙️"
        else:
            return "📄"
    
    def _on_select(self, event):
        """Handle tree item selection."""
        pass
    
    def _open_in_file_manager(self):
        """Open output directory in system file manager."""
        if not self.current_path:
            return
        
        import subprocess
        import platform
        
        system = platform.system()
        try:
            if system == "Windows":
                os.startfile(self.current_path)
            elif system == "Darwin":
                subprocess.run(["open", self.current_path])
            else:
                subprocess.run(["xdg-open", self.current_path])
        except Exception:
            pass
    
    def refresh(self):
        """Refresh the tree view."""
        if self.current_path:
            self.load_directory(self.current_path)
    
    def clear(self):
        """Clear the tree view."""
        self.tree.delete(*self.tree.get_children())
        self.current_path = None
        self.open_btn.configure(state="disabled")
        self.refresh_btn.configure(state="disabled")
