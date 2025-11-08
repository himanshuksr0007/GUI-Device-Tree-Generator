#!/usr/bin/env python3
"""
Build script for creating standalone executables of GUI Device Tree Generator.
Supports Windows, Linux, and macOS platforms.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

VERSION = "1.0.0"
APP_NAME = "GUI-Device-Tree-Generator"
MAIN_SCRIPT = "src/main.py"
ICON_FILE = "assets/icon.ico" if platform.system() == "Windows" else "assets/icon.icns"

def clean_build():
    """Remove previous build artifacts."""
    print("Cleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed {dir_name}/")
    
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"  Removed {spec_file}")

def get_pyinstaller_args():
    """Get platform-specific PyInstaller arguments."""
    system = platform.system()
    
    base_args = [
        'pyinstaller',
        '--name', APP_NAME,
        '--onefile',
        '--windowed' if system == 'Windows' else '--console',
        '--clean',
        '--noconfirm',
    ]
    
    data_files = [
        '--add-data', f'src{os.pathsep}src',
    ]
    
    hidden_imports = [
        '--hidden-import', 'customtkinter',
        '--hidden-import', 'PIL',
        '--hidden-import', 'PIL._tkinter_finder',
        '--hidden-import', 'twrpdtgen',
        '--hidden-import', 'psutil',
    ]
    
    if system == 'Windows':
        if os.path.exists('assets/icon.ico'):
            base_args.extend(['--icon', 'assets/icon.ico'])
        base_args.extend([
            '--version-file', 'version_info.txt' if os.path.exists('version_info.txt') else None
        ])
    elif system == 'Darwin':
        if os.path.exists('assets/icon.icns'):
            base_args.extend(['--icon', 'assets/icon.icns'])
    
    base_args = [arg for arg in base_args if arg is not None]
    
    return base_args + data_files + hidden_imports + [MAIN_SCRIPT]

def build_executable():
    """Build the executable using PyInstaller."""
    print(f"\nBuilding {APP_NAME} v{VERSION} for {platform.system()}...\n")
    
    try:
        import PyInstaller
        print(f"Using PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("ERROR: PyInstaller not found. Install it with: pip install pyinstaller")
        sys.exit(1)
    
    args = get_pyinstaller_args()
    print("PyInstaller arguments:")
    print(" ".join(args))
    print()
    
    try:
        subprocess.run(args, check=True)
        print(f"\n{'-'*60}")
        print(f"Build completed successfully!")
        print(f"Executable location: dist/{APP_NAME}{'exe' if platform.system() == 'Windows' else ''}")
        print(f"{'-'*60}\n")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed with exit code {e.returncode}")
        sys.exit(1)

def create_version_info():
    """Create Windows version info file."""
    if platform.system() != 'Windows':
        return
    
    version_info = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION.replace('.', ', ')}, 0),
    prodvers=({VERSION.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Himanshu Kumar'),
        StringStruct(u'FileDescription', u'GUI Device Tree Generator'),
        StringStruct(u'FileVersion', u'{VERSION}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2025 Himanshu Kumar. MIT License.'),
        StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
        StringStruct(u'ProductName', u'GUI Device Tree Generator'),
        StringStruct(u'ProductVersion', u'{VERSION}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
    print("Created version_info.txt for Windows build")

def create_dist_package():
    """Create a distributable package."""
    print("\nCreating distribution package...")
    
    system = platform.system()
    dist_dir = Path('dist')
    package_name = f"{APP_NAME}-v{VERSION}-{system}-{platform.machine()}"
    package_dir = dist_dir / package_name
    
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir(parents=True, exist_ok=True)
    
    exe_name = f"{APP_NAME}.exe" if system == 'Windows' else APP_NAME
    exe_path = dist_dir / exe_name
    
    if exe_path.exists():
        shutil.copy(exe_path, package_dir / exe_name)
        print(f"  Copied {exe_name}")
    
    docs_to_copy = ['README.md', 'LICENSE']
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy(doc, package_dir / doc)
            print(f"  Copied {doc}")
    
    if system == 'Windows':
        archive_format = 'zip'
    else:
        archive_format = 'gztar'
    
    archive_path = shutil.make_archive(
        str(dist_dir / package_name),
        archive_format,
        dist_dir,
        package_name
    )
    
    shutil.rmtree(package_dir)
    
    print(f"\nDistribution package created: {archive_path}")
    print(f"Size: {os.path.getsize(archive_path) / (1024*1024):.2f} MB")

def main():
    """Main build process."""
    print(f"""
{'='*60}
  GUI Device Tree Generator - Build Script
  Version: {VERSION}
  Platform: {platform.system()} {platform.machine()}
  Python: {sys.version.split()[0]}
{'='*60}
    """)
    
    if not os.path.exists(MAIN_SCRIPT):
        print(f"ERROR: Main script not found: {MAIN_SCRIPT}")
        sys.exit(1)
    
    if '--clean-only' in sys.argv:
        clean_build()
        return
    
    clean_build()
    
    if platform.system() == 'Windows':
        create_version_info()
    
    build_executable()
    
    if '--package' in sys.argv:
        create_dist_package()
    
    print("\n✓ Build process completed successfully!\n")

if __name__ == "__main__":
    main()
