#!/usr/bin/env python3
"""
Progress Panel - Real-time progress visualization with steps
"""

import customtkinter as ctk
from typing import List, Optional


class ProgressStep(ctk.CTkFrame):
    """Individual progress step indicator."""
    
    def __init__(self, parent, step_num: int, title: str, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.step_num = step_num
        self.title = title
        self.state = "pending"  # pending, active, complete, error
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup step UI."""
        self.circle = ctk.CTkLabel(
            self,
            text=str(self.step_num),
            width=35,
            height=35,
            font=("Helvetica", 12, "bold"),
            fg_color="#3a3a3a",
            corner_radius=17
        )
        self.circle.pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        self.title_label = ctk.CTkLabel(
            text_frame,
            text=self.title,
            font=("Helvetica", 11),
            anchor="w"
        )
        self.title_label.pack(anchor="w")
        
        self.status_label = ctk.CTkLabel(
            text_frame,
            text="Pending",
            font=("Helvetica", 9),
            text_color="gray",
            anchor="w"
        )
        self.status_label.pack(anchor="w")
    
    def set_active(self):
        """Mark step as active."""
        self.state = "active"
        self.circle.configure(fg_color="#2196F3")
        self.status_label.configure(text="In Progress...", text_color="#2196F3")
    
    def set_complete(self):
        """Mark step as complete."""
        self.state = "complete"
        self.circle.configure(fg_color="#4CAF50", text="✓")
        self.status_label.configure(text="Complete", text_color="#4CAF50")
    
    def set_error(self, message: str = "Error"):
        """Mark step as error."""
        self.state = "error"
        self.circle.configure(fg_color="#F44336", text="✗")
        self.status_label.configure(text=message, text_color="#F44336")
    
    def reset(self):
        """Reset step to pending state."""
        self.state = "pending"
        self.circle.configure(fg_color="#3a3a3a", text=str(self.step_num))
        self.status_label.configure(text="Pending", text_color="gray")


class ProgressPanel(ctk.CTkFrame):
    """Progress panel with step-by-step visualization."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.steps: List[ProgressStep] = []
        self.current_step = -1
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup progress panel UI."""
        title = ctk.CTkLabel(
            self,
            text="📊 Generation Progress",
            font=("Helvetica", 14, "bold")
        )
        title.pack(pady=(10, 10), padx=15, anchor="w")
        
        self.steps_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.steps_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        step_titles = [
            "Validating Image",
            "Extracting Boot Image",
            "Parsing Device Info",
            "Analyzing Partitions",
            "Generating Makefiles",
            "Creating Device Tree",
            "Validating Output"
        ]
        
        for i, title in enumerate(step_titles, 1):
            step = ProgressStep(self.steps_frame, i, title)
            step.pack(fill="x", pady=3)
            self.steps.append(step)
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=(10, 5), padx=15)
        self.progress_bar.set(0)
        
        self.percentage_label = ctk.CTkLabel(
            self,
            text="0%",
            font=("Helvetica", 10)
        )
        self.percentage_label.pack(pady=(0, 10))
    
    def set_step(self, step_num: int, status: str = "active"):
        """Set the current step status."""
        if step_num < 1 or step_num > len(self.steps):
            return
        
        if self.current_step > 0 and self.current_step <= len(self.steps):
            if status != "error":
                self.steps[self.current_step - 1].set_complete()
        
        self.current_step = step_num
        
        if status == "active":
            self.steps[step_num - 1].set_active()
        elif status == "error":
            self.steps[step_num - 1].set_error()
        
        progress = step_num / len(self.steps)
        self.progress_bar.set(progress)
        self.percentage_label.configure(text=f"{int(progress * 100)}%")
    
    def set_error(self, step_num: int, message: str):
        """Set error state for a step."""
        if step_num < 1 or step_num > len(self.steps):
            return
        self.steps[step_num - 1].set_error(message)
    
    def complete_all(self):
        """Mark all steps as complete."""
        for step in self.steps:
            step.set_complete()
        self.progress_bar.set(1.0)
        self.percentage_label.configure(text="100%")
    
    def reset(self):
        """Reset all steps to pending."""
        for step in self.steps:
            step.reset()
        self.current_step = -1
        self.progress_bar.set(0)
        self.percentage_label.configure(text="0%")
