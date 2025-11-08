#!/usr/bin/env python3
"""
Device Tree Processor - Core Processing Logic

Handles boot image processing and device tree generation.
"""

import os
import sys
import shutil
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Dict, Callable, Optional, Any
import time


class DeviceTreeProcessor:
    """Main processor for device tree generation."""
    
    def __init__(self):
        self.temp_dir = None
        self.work_dir = None
    
    def process_image(
        self,
        image_path: str,
        output_dir: str,
        tree_type: str = "twrp",
        init_git: bool = True,
        validate: bool = True,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Process boot image and generate device tree.
        
        Args:
            image_path: Path to boot/recovery image
            output_dir: Output directory for generated device tree
            tree_type: Type of device tree (twrp, lineageos)
            init_git: Initialize git repository
            validate: Validate generated device tree
            progress_callback: Callback for progress updates
            log_callback: Callback for log messages
        
        Returns:
            Dict containing success status, output path, and device info
        """
        try:
            self._create_work_directory()
            
            if log_callback:
                log_callback("Initializing device tree generation...")
            
            if tree_type == "twrp":
                result = self._process_with_twrpdtgen(
                    image_path, output_dir, init_git,
                    progress_callback, log_callback
                )
            else:
                return {
                    'success': False,
                    'error': f"Tree type '{tree_type}' not yet supported. Use 'twrp' for now."
                }
            
            if result['success'] and validate:
                if progress_callback:
                    progress_callback(0.9, "Validating device tree...")
                if log_callback:
                    log_callback("Validating generated device tree...")
                
                validation = self._validate_device_tree(result['output_path'])
                result['validation'] = validation
                
                if not validation['valid']:
                    if log_callback:
                        log_callback(f"Warning: Validation issues found: {', '.join(validation['warnings'])}")
            
            return result
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            self._cleanup_work_directory()
    
    def _create_work_directory(self):
        """Create temporary working directory."""
        self.temp_dir = tempfile.mkdtemp(prefix="dtgen_")
        self.work_dir = Path(self.temp_dir)
    
    def _cleanup_work_directory(self):
        """Cleanup temporary working directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception:
                pass
    
    def _process_with_twrpdtgen(
        self,
        image_path: str,
        output_dir: str,
        init_git: bool,
        progress_callback: Optional[Callable],
        log_callback: Optional[Callable]
    ) -> Dict[str, Any]:
        """
        Process image using twrpdtgen.
        
        This method integrates with the twrpdtgen CLI tool to generate
        TWRP-compatible device trees.
        """
        try:
            if not self._check_twrpdtgen_installed():
                return {
                    'success': False,
                    'error': 'twrpdtgen not installed. Install with: pip install twrpdtgen'
                }
            
            if progress_callback:
                progress_callback(0.3, "Extracting boot image...")
            if log_callback:
                log_callback("Extracting boot image contents...")
            
            os.makedirs(output_dir, exist_ok=True)
            
            cmd = [
                sys.executable, "-m", "twrpdtgen",
                image_path,
                "-o", output_dir
            ]
            
            if log_callback:
                log_callback(f"Running: {' '.join(cmd)}")
            
            if progress_callback:
                progress_callback(0.4, "Analyzing device information...")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout_lines = []
            stderr_lines = []
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    stdout_lines.append(line)
                    if log_callback:
                        log_callback(line)
            
            for line in process.stderr:
                line = line.strip()
                if line:
                    stderr_lines.append(line)
            
            process.wait()
            
            if process.returncode != 0:
                error_msg = "\n".join(stderr_lines) if stderr_lines else "Unknown error during generation"
                return {
                    'success': False,
                    'error': f"twrpdtgen failed: {error_msg}"
                }
            
            if progress_callback:
                progress_callback(0.7, "Generating device tree files...")
            if log_callback:
                log_callback("Device tree files generated successfully")
            
            device_info = self._extract_device_info(output_dir)
            
            if init_git:
                if progress_callback:
                    progress_callback(0.85, "Initializing git repository...")
                if log_callback:
                    log_callback("Initializing git repository...")
                
                self._initialize_git(output_dir, log_callback)
            
            return {
                'success': True,
                'output_path': output_dir,
                'device_name': device_info.get('device', 'Unknown'),
                'manufacturer': device_info.get('manufacturer', 'Unknown'),
                'device_info': device_info
            }
        
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'twrpdtgen not found. Please install it with: pip install twrpdtgen'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error during processing: {str(e)}"
            }
    
    def _check_twrpdtgen_installed(self) -> bool:
        """Check if twrpdtgen is installed."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "twrpdtgen", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _extract_device_info(self, output_dir: str) -> Dict[str, str]:
        """
        Extract device information from generated device tree.
        
        Parses the generated files to extract device codename,
        manufacturer, and other relevant information.
        """
        device_info = {
            'device': 'Unknown',
            'manufacturer': 'Unknown',
            'model': 'Unknown',
            'architecture': 'Unknown'
        }
        
        try:
            output_path = Path(output_dir)
            
            for item in output_path.iterdir():
                if item.is_dir():
                    manufacturer = item.name
                    device_info['manufacturer'] = manufacturer
                    
                    for device_dir in item.iterdir():
                        if device_dir.is_dir():
                            device_info['device'] = device_dir.name
                            
                            boardconfig = device_dir / "BoardConfig.mk"
                            if boardconfig.exists():
                                with open(boardconfig, 'r') as f:
                                    content = f.read()
                                    
                                    if 'TARGET_ARCH := arm64' in content:
                                        device_info['architecture'] = 'arm64'
                                    elif 'TARGET_ARCH := arm' in content:
                                        device_info['architecture'] = 'arm'
                                    elif 'TARGET_ARCH := x86_64' in content:
                                        device_info['architecture'] = 'x86_64'
                                    elif 'TARGET_ARCH := x86' in content:
                                        device_info['architecture'] = 'x86'
                            
                            break
                    break
        
        except Exception as e:
            pass
        
        return device_info
    
    def _initialize_git(self, directory: str, log_callback: Optional[Callable] = None):
        """
        Initialize git repository in the output directory.
        """
        try:
            result = subprocess.run(
                ['git', 'init'],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                subprocess.run(
                    ['git', 'add', '.'],
                    cwd=directory,
                    capture_output=True,
                    timeout=10
                )
                
                subprocess.run(
                    ['git', 'commit', '-m', 'Initial device tree generation'],
                    cwd=directory,
                    capture_output=True,
                    timeout=10
                )
                
                if log_callback:
                    log_callback("Git repository initialized successfully")
            else:
                if log_callback:
                    log_callback("Warning: Git initialization failed (git may not be installed)")
        
        except FileNotFoundError:
            if log_callback:
                log_callback("Warning: Git not found. Skipping git initialization.")
        except Exception as e:
            if log_callback:
                log_callback(f"Warning: Git initialization error: {str(e)}")
    
    def _validate_device_tree(self, output_dir: str) -> Dict[str, Any]:
        """
        Validate the generated device tree.
        
        Checks for required files and common issues.
        """
        validation = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        required_files = [
            'BoardConfig.mk',
            'Android.mk',
            'AndroidProducts.mk'
        ]
        
        try:
            output_path = Path(output_dir)
            
            for item in output_path.iterdir():
                if item.is_dir():
                    for device_dir in item.iterdir():
                        if device_dir.is_dir():
                            for required_file in required_files:
                                file_path = device_dir / required_file
                                if not file_path.exists():
                                    validation['warnings'].append(
                                        f"Missing file: {required_file}"
                                    )
                            
                            recovery_fstab = device_dir / "recovery" / "root" / "system" / "etc" / "recovery.fstab"
                            if not recovery_fstab.exists():
                                alt_fstab = device_dir / "recovery.fstab"
                                if not alt_fstab.exists():
                                    validation['warnings'].append(
                                        "Missing recovery.fstab file"
                                    )
                            
                            break
                    break
            
            if validation['warnings']:
                validation['valid'] = False
        
        except Exception as e:
            validation['errors'].append(f"Validation error: {str(e)}")
            validation['valid'] = False
        
        return validation
