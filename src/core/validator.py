#!/usr/bin/env python3
"""
Image Validator - Validates boot/recovery images

Validates that the selected file is a valid boot or recovery image.
"""

import os
import mimetypes
from pathlib import Path
from typing import Dict, Any


class ImageValidator:
    """Validator for boot/recovery images."""
    
    VALID_EXTENSIONS = ['.img', '.tar', '.gz', '.lz4', '.zip']
    MIN_SIZE_MB = 1
    MAX_SIZE_MB = 500
    
    def __init__(self):
        self.magic_bytes = {
            'android_boot': b'ANDROID!',
            'gzip': b'\x1f\x8b',
            'lz4': b'\x04\x22\x4d\x18',
            'tar': b'ustar'
        }
    
    def validate_image(self, filepath: str) -> Dict[str, Any]:
        """
        Validate that the file is a valid boot/recovery image.
        
        Args:
            filepath: Path to the image file
        
        Returns:
            Dict with validation result and details
        """
        if not os.path.exists(filepath):
            return {
                'valid': False,
                'message': 'File does not exist',
                'type': None
            }
        
        if not os.path.isfile(filepath):
            return {
                'valid': False,
                'message': 'Path is not a file',
                'type': None
            }
        
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        
        if file_size_mb < self.MIN_SIZE_MB:
            return {
                'valid': False,
                'message': f'File too small ({file_size_mb:.2f} MB). Minimum size: {self.MIN_SIZE_MB} MB',
                'type': None
            }
        
        if file_size_mb > self.MAX_SIZE_MB:
            return {
                'valid': False,
                'message': f'File too large ({file_size_mb:.2f} MB). Maximum size: {self.MAX_SIZE_MB} MB',
                'type': None
            }
        
        extension = Path(filepath).suffix.lower()
        if extension not in self.VALID_EXTENSIONS:
            return {
                'valid': False,
                'message': f'Invalid file extension: {extension}. Supported: {", ".join(self.VALID_EXTENSIONS)}',
                'type': None
            }
        
        file_type = self._detect_file_type(filepath)
        
        return {
            'valid': True,
            'message': 'Valid boot/recovery image',
            'type': file_type,
            'size_mb': file_size_mb
        }
    
    def _detect_file_type(self, filepath: str) -> str:
        """
        Detect the specific type of boot image file.
        
        Args:
            filepath: Path to the image file
        
        Returns:
            String describing the file type
        """
        try:
            with open(filepath, 'rb') as f:
                header = f.read(512)
            
            if self.magic_bytes['android_boot'] in header:
                return 'Android Boot Image'
            elif header.startswith(self.magic_bytes['gzip']):
                return 'GZip Compressed Image'
            elif header.startswith(self.magic_bytes['lz4']):
                return 'LZ4 Compressed Image'
            elif self.magic_bytes['tar'] in header:
                return 'TAR Archive'
            else:
                extension = Path(filepath).suffix.lower()
                if extension == '.img':
                    return 'Raw Image File'
                elif extension == '.zip':
                    return 'ZIP Archive'
                else:
                    return 'Unknown Format'
        
        except Exception:
            return 'Unknown Format'
    
    def get_image_info(self, filepath: str) -> Dict[str, Any]:
        """
        Get detailed information about the image file.
        
        Args:
            filepath: Path to the image file
        
        Returns:
            Dict with file information
        """
        if not os.path.exists(filepath):
            return {}
        
        stat = os.stat(filepath)
        
        return {
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified_time': stat.st_mtime,
            'extension': Path(filepath).suffix.lower(),
            'type': self._detect_file_type(filepath)
        }
