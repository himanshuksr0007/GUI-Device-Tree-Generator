#!/usr/bin/env python3
"""
GUI Device Tree Generator - Main Entry Point

A modern graphical interface for generating Android device trees from boot/recovery images.
Author: Himanshu Kumar
License: MIT
"""

import sys
import os
import tkinter as tk
from pathlib import Path

try:
    import customtkinter as ctk
except ImportError:
    print("Error: CustomTkinter not installed. Install with: pip install customtkinter")
    sys.exit(1)

from gui.main_window import DeviceTreeGeneratorApp

def setup_environment():
    """Setup environment variables and paths."""
    if getattr(sys, 'frozen', False):
        application_path = Path(sys.executable).parent
    else:
        application_path = Path(__file__).parent.parent
    
    os.chdir(application_path)
    return application_path

def main():
    """Main application entry point."""
    try:
        app_path = setup_environment()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        root = ctk.CTk()
        app = DeviceTreeGeneratorApp(root)
        
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
