#!/usr/bin/env python3
"""
TWRP Extractor - Wrapper for twrpdtgen
"""

import subprocess
import sys
from typing import Dict, Any, Optional, Callable


class TWRPExtractor:
    """Wrapper for twrpdtgen tool."""
    
    def __init__(self):
        self.twrpdtgen_available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if twrpdtgen is installed."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "twrpdtgen", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def extract(self, image_path: str, output_dir: str, 
                progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Extract device tree using twrpdtgen."""
        if not self.twrpdtgen_available:
            return {
                'success': False,
                'error': 'twrpdtgen not installed'
            }
        
        try:
            cmd = [sys.executable, "-m", "twrpdtgen", image_path, "-o", output_dir]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                return {
                    'success': True,
                    'output': stdout
                }
            else:
                return {
                    'success': False,
                    'error': stderr or 'Unknown error'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
