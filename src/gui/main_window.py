#!/usr/bin/env python3
"""
Main Application Window - GUI Device Tree Generator

This module contains the main application window and all GUI logic.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import customtkinter as ctk
from typing import Optional

from core.processor import DeviceTreeProcessor
from core.validator import ImageValidator
from utils.logger import Logger


class DeviceTreeGeneratorApp:
    """Main application window for GUI Device Tree Generator."""
    
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("GUI Device Tree Generator v1.0")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)
        
        self.processor = DeviceTreeProcessor()
        self.validator = ImageValidator()
        self.logger = Logger()
        
        self.selected_image_path: Optional[str] = None
        self.output_directory: Optional[str] = None
        self.is_processing = False
        
        self._setup_ui()
        self._setup_drag_drop()
        
    def _setup_ui(self):
        """Setup the main user interface."""
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_container,
            text="GUI Device Tree Generator",
            font=("Helvetica", 28, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_container,
            text="Generate Android device trees from boot/recovery images",
            font=("Helvetica", 12)
        )
        subtitle_label.pack(pady=(0, 20))
        
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True)
        
        self._create_input_section(content_frame)
        self._create_options_section(content_frame)
        self._create_action_section(content_frame)
        self._create_progress_section(content_frame)
        self._create_log_section(content_frame)
        
    def _create_input_section(self, parent):
        """Create the file input section."""
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        header = ctk.CTkLabel(
            input_frame,
            text="📁 Boot Image Selection",
            font=("Helvetica", 16, "bold")
        )
        header.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.drop_zone = ctk.CTkFrame(input_frame, height=100, corner_radius=10)
        self.drop_zone.pack(fill="x", padx=15, pady=10)
        
        drop_label = ctk.CTkLabel(
            self.drop_zone,
            text="Drag & Drop boot.img / recovery.img here\nor click 'Select Image' below",
            font=("Helvetica", 13)
        )
        drop_label.pack(expand=True, pady=30)
        
        self.selected_file_label = ctk.CTkLabel(
            input_frame,
            text="No file selected",
            font=("Helvetica", 11),
            text_color="gray"
        )
        self.selected_file_label.pack(padx=15, pady=(0, 5))
        
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        select_btn = ctk.CTkButton(
            button_frame,
            text="Select Image",
            command=self.select_image,
            width=150,
            height=35
        )
        select_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_selection,
            width=100,
            height=35,
            fg_color="#8B0000",
            hover_color="#A52A2A"
        )
        clear_btn.pack(side="left")
        
    def _create_options_section(self, parent):
        """Create the options configuration section."""
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        header = ctk.CTkLabel(
            options_frame,
            text="⚙️ Configuration Options",
            font=("Helvetica", 16, "bold")
        )
        header.pack(anchor="w", padx=15, pady=(10, 5))
        
        content = ctk.CTkFrame(options_frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        
        output_label = ctk.CTkLabel(content, text="Output Directory:", font=("Helvetica", 12))
        output_label.grid(row=0, column=0, sticky="w", pady=5)
        
        output_btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        output_btn_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        content.columnconfigure(1, weight=1)
        
        self.output_path_label = ctk.CTkLabel(
            output_btn_frame,
            text="./output (default)",
            font=("Helvetica", 11),
            text_color="gray"
        )
        self.output_path_label.pack(side="left", padx=(0, 10))
        
        output_btn = ctk.CTkButton(
            output_btn_frame,
            text="Browse",
            command=self.select_output_directory,
            width=100
        )
        output_btn.pack(side="right")
        
        tree_label = ctk.CTkLabel(content, text="Device Tree Type:", font=("Helvetica", 12))
        tree_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.tree_type_var = tk.StringVar(value="twrp")
        tree_dropdown = ctk.CTkOptionMenu(
            content,
            values=["TWRP", "LineageOS (Coming Soon)"],
            variable=self.tree_type_var,
            width=200
        )
        tree_dropdown.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)
        
        self.init_git_var = tk.BooleanVar(value=True)
        git_checkbox = ctk.CTkCheckBox(
            content,
            text="Initialize Git repository",
            variable=self.init_git_var,
            font=("Helvetica", 11)
        )
        git_checkbox.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)
        
        self.validate_var = tk.BooleanVar(value=True)
        validate_checkbox = ctk.CTkCheckBox(
            content,
            text="Validate generated device tree",
            variable=self.validate_var,
            font=("Helvetica", 11)
        )
        validate_checkbox.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
        
    def _create_action_section(self, parent):
        """Create the action buttons section."""
        action_frame = ctk.CTkFrame(parent, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=10)
        
        self.generate_btn = ctk.CTkButton(
            action_frame,
            text="🚀 Generate Device Tree",
            command=self.start_generation,
            height=45,
            font=("Helvetica", 14, "bold"),
            fg_color="#2E7D32",
            hover_color="#388E3C"
        )
        self.generate_btn.pack(fill="x", padx=10)
        
    def _create_progress_section(self, parent):
        """Create the progress tracking section."""
        progress_frame = ctk.CTkFrame(parent)
        progress_frame.pack(fill="x", padx=10, pady=10)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to generate device tree",
            font=("Helvetica", 12)
        )
        self.progress_label.pack(pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=500)
        self.progress_bar.pack(pady=(0, 10), padx=20)
        self.progress_bar.set(0)
        
    def _create_log_section(self, parent):
        """Create the log viewer section."""
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = ctk.CTkLabel(
            log_frame,
            text="📋 Generation Log",
            font=("Helvetica", 14, "bold")
        )
        header.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(log_frame, height=150, font=("Courier", 10))
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        self.log_text.configure(state="disabled")
        
    def _setup_drag_drop(self):
        """Setup drag and drop functionality."""
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            self.drop_zone.drop_target_register(DND_FILES)
            self.drop_zone.dnd_bind('<<Drop>>', self.on_drop)
        except ImportError:
            pass
    
    def select_image(self):
        """Open file dialog to select boot image."""
        file_types = [
            ("Image Files", "*.img *.tar *.gz *.lz4"),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Boot/Recovery Image",
            filetypes=file_types
        )
        
        if filename:
            self.set_selected_image(filename)
    
    def select_output_directory(self):
        """Open dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        
        if directory:
            self.output_directory = directory
            self.output_path_label.configure(text=directory)
            self.log_message(f"Output directory set to: {directory}")
    
    def set_selected_image(self, filepath: str):
        """Set the selected image file."""
        if not os.path.exists(filepath):
            self.show_error("File not found", f"The file {filepath} does not exist.")
            return
        
        validation_result = self.validator.validate_image(filepath)
        
        if not validation_result['valid']:
            self.show_error("Invalid Image", validation_result['message'])
            return
        
        self.selected_image_path = filepath
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath) / (1024 * 1024)
        
        self.selected_file_label.configure(
            text=f"✓ {filename} ({filesize:.2f} MB)",
            text_color="#4CAF50"
        )
        
        self.log_message(f"Selected image: {filename}")
        self.log_message(f"File size: {filesize:.2f} MB")
        self.log_message(f"File type: {validation_result['type']}")
    
    def clear_selection(self):
        """Clear the selected image."""
        self.selected_image_path = None
        self.selected_file_label.configure(
            text="No file selected",
            text_color="gray"
        )
        self.log_message("Selection cleared")
    
    def on_drop(self, event):
        """Handle drag and drop event."""
        filepath = event.data
        if filepath.startswith('{') and filepath.endswith('}'):
            filepath = filepath[1:-1]
        
        self.set_selected_image(filepath)
    
    def start_generation(self):
        """Start the device tree generation process."""
        if self.is_processing:
            self.show_warning("Already Processing", "Please wait for the current process to complete.")
            return
        
        if not self.selected_image_path:
            self.show_warning("No Image Selected", "Please select a boot or recovery image first.")
            return
        
        self.is_processing = True
        self.generate_btn.configure(state="disabled", text="⏳ Generating...")
        self.progress_bar.set(0)
        self.clear_log()
        
        thread = threading.Thread(target=self._run_generation, daemon=True)
        thread.start()
    
    def _run_generation(self):
        """Run the generation process in a separate thread."""
        try:
            output_dir = self.output_directory or "./output"
            
            self.update_progress(0.1, "Validating image...")
            self.log_message("Starting device tree generation...")
            self.log_message(f"Input: {self.selected_image_path}")
            self.log_message(f"Output: {output_dir}")
            
            self.update_progress(0.2, "Extracting boot image...")
            
            result = self.processor.process_image(
                image_path=self.selected_image_path,
                output_dir=output_dir,
                tree_type=self.tree_type_var.get().lower().split()[0],
                init_git=self.init_git_var.get(),
                validate=self.validate_var.get(),
                progress_callback=self.update_progress,
                log_callback=self.log_message
            )
            
            if result['success']:
                self.update_progress(1.0, "✓ Device tree generated successfully!")
                self.log_message("\n" + "="*60)
                self.log_message("SUCCESS: Device tree generated!")
                self.log_message(f"Location: {result['output_path']}")
                self.log_message(f"Device: {result.get('device_name', 'Unknown')}")
                self.log_message("="*60)
                
                self.root.after(0, lambda: self.show_success(
                    "Generation Complete",
                    f"Device tree successfully generated!\n\nLocation: {result['output_path']}"
                ))
            else:
                self.update_progress(0, "✗ Generation failed")
                self.log_message(f"\nERROR: {result['error']}")
                
                self.root.after(0, lambda: self.show_error(
                    "Generation Failed",
                    f"An error occurred:\n\n{result['error']}"
                ))
        
        except Exception as e:
            self.update_progress(0, "✗ Fatal error occurred")
            self.log_message(f"\nFATAL ERROR: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())
            
            self.root.after(0, lambda: self.show_error(
                "Fatal Error",
                f"An unexpected error occurred:\n\n{str(e)}"
            ))
        
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.generate_btn.configure(
                state="normal",
                text="🚀 Generate Device Tree"
            ))
    
    def update_progress(self, value: float, message: str = ""):
        """Update progress bar and message."""
        def update():
            self.progress_bar.set(value)
            if message:
                self.progress_label.configure(text=message)
        
        self.root.after(0, update)
    
    def log_message(self, message: str):
        """Add message to log viewer."""
        def add_log():
            self.log_text.configure(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        
        self.root.after(0, add_log)
        self.logger.log(message)
    
    def clear_log(self):
        """Clear the log viewer."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
    
    def show_success(self, title: str, message: str):
        """Show success message box."""
        messagebox.showinfo(title, message)
    
    def show_error(self, title: str, message: str):
        """Show error message box."""
        messagebox.showerror(title, message)
    
    def show_warning(self, title: str, message: str):
        """Show warning message box."""
        messagebox.showwarning(title, message)
    
    def on_closing(self):
        """Handle window close event."""
        if self.is_processing:
            if messagebox.askyesno(
                "Confirm Exit",
                "Generation is in progress. Are you sure you want to exit?"
            ):
                self.root.destroy()
        else:
            self.root.destroy()
