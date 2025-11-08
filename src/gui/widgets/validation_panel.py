#!/usr/bin/env python3
"""
Validation Panel - Device tree validation dashboard with checks
"""

import customtkinter as ctk
from typing import List, Dict, Any


class ValidationItem(ctk.CTkFrame):
    """Individual validation check item."""
    
    def __init__(self, parent, check_name: str, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.check_name = check_name
        self.status = "pending"  # pending, pass, fail, warning
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup validation item UI."""
        self.icon_label = ctk.CTkLabel(
            self,
            text="⏳",
            font=("Helvetica", 16),
            width=30
        )
        self.icon_label.pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        self.name_label = ctk.CTkLabel(
            text_frame,
            text=self.check_name,
            font=("Helvetica", 11),
            anchor="w"
        )
        self.name_label.pack(anchor="w")
        
        self.detail_label = ctk.CTkLabel(
            text_frame,
            text="Pending validation...",
            font=("Helvetica", 9),
            text_color="gray",
            anchor="w"
        )
        self.detail_label.pack(anchor="w")
    
    def set_pass(self, message: str = "Check passed"):
        """Mark validation as passed."""
        self.status = "pass"
        self.icon_label.configure(text="✓", text_color="#4CAF50")
        self.detail_label.configure(text=message, text_color="#4CAF50")
    
    def set_fail(self, message: str = "Check failed"):
        """Mark validation as failed."""
        self.status = "fail"
        self.icon_label.configure(text="✗", text_color="#F44336")
        self.detail_label.configure(text=message, text_color="#F44336")
    
    def set_warning(self, message: str = "Warning"):
        """Mark validation as warning."""
        self.status = "warning"
        self.icon_label.configure(text="⚠", text_color="#FF9800")
        self.detail_label.configure(text=message, text_color="#FF9800")
    
    def reset(self):
        """Reset validation status."""
        self.status = "pending"
        self.icon_label.configure(text="⏳", text_color="gray")
        self.detail_label.configure(text="Pending validation...", text_color="gray")


class ValidationPanel(ctk.CTkFrame):
    """Validation dashboard for device tree checks."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.validation_items: Dict[str, ValidationItem] = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup validation panel UI."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title = ctk.CTkLabel(
            header_frame,
            text="✔️ Validation Checks",
            font=("Helvetica", 14, "bold")
        )
        title.pack(side="left")
        
        self.summary_label = ctk.CTkLabel(
            header_frame,
            text="0/0 checks passed",
            font=("Helvetica", 10),
            text_color="gray"
        )
        self.summary_label.pack(side="right")
        
        scrollable_frame = ctk.CTkScrollableFrame(self, height=250)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.checks_frame = scrollable_frame
        
        validation_checks = [
            "Required Files Present",
            "BoardConfig.mk Syntax",
            "Android.mk Syntax",
            "Device.mk Syntax",
            "Recovery Fstab Valid",
            "Partition Scheme",
            "Kernel Configuration",
            "Vendor Blob List",
            "Build System Compatible"
        ]
        
        for check_name in validation_checks:
            item = ValidationItem(self.checks_frame, check_name)
            item.pack(fill="x", pady=3)
            self.validation_items[check_name] = item
        
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        validate_btn = ctk.CTkButton(
            action_frame,
            text="Run Validation",
            command=self._on_validate,
            width=120,
            height=32
        )
        validate_btn.pack(side="left", padx=(0, 10))
        
        export_btn = ctk.CTkButton(
            action_frame,
            text="Export Report",
            command=self._on_export,
            width=120,
            height=32
        )
        export_btn.pack(side="left")
    
    def run_validation(self, results: Dict[str, Dict[str, Any]]):
        """Run validation with provided results."""
        for check_name, result in results.items():
            if check_name in self.validation_items:
                item = self.validation_items[check_name]
                
                status = result.get('status', 'pending')
                message = result.get('message', '')
                
                if status == 'pass':
                    item.set_pass(message)
                elif status == 'fail':
                    item.set_fail(message)
                elif status == 'warning':
                    item.set_warning(message)
        
        self._update_summary()
    
    def _update_summary(self):
        """Update the validation summary."""
        total = len(self.validation_items)
        passed = sum(1 for item in self.validation_items.values() if item.status == "pass")
        failed = sum(1 for item in self.validation_items.values() if item.status == "fail")
        warnings = sum(1 for item in self.validation_items.values() if item.status == "warning")
        
        summary_text = f"{passed}/{total} passed"
        if failed > 0:
            summary_text += f", {failed} failed"
        if warnings > 0:
            summary_text += f", {warnings} warnings"
        
        self.summary_label.configure(text=summary_text)
    
    def reset(self):
        """Reset all validation checks."""
        for item in self.validation_items.values():
            item.reset()
        self.summary_label.configure(text="0/0 checks passed")
    
    def _on_validate(self):
        """Handle validate button click."""
        pass
    
    def _on_export(self):
        """Handle export button click."""
        pass
