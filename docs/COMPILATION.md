# Compilation Guide - Building Executables

This guide explains how to compile the GUI Device Tree Generator into standalone executables for Windows, Linux, and macOS.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Windows Compilation](#windows-compilation)
3. [Linux Compilation](#linux-compilation)
4. [macOS Compilation](#macos-compilation)
5. [Advanced Configuration](#advanced-configuration)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### All Platforms

1. **Python 3.9 or higher**
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Git** (for cloning the repository)
   ```bash
   git --version
   ```

3. **Project source code**
   ```bash
   git clone https://github.com/himanshuksr0007/GUI-Device-Tree-Generator.git
   cd GUI-Device-Tree-Generator
   ```

4. **Virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

## Windows Compilation

### Step 1: Prepare Environment

```cmd
cd GUI-Device-Tree-Generator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

### Step 2: Build Executable

```cmd
python build_exe.py
```

This will:
- Clean previous build artifacts
- Create Windows version info
- Build the executable
- Output to `dist/GUI-Device-Tree-Generator.exe`

### Step 3: Test Executable

```cmd
cd dist
GUI-Device-Tree-Generator.exe
```

### Step 4: Create Distribution Package

```cmd
python build_exe.py --package
```

This creates a ZIP file: `dist/GUI-Device-Tree-Generator-v1.0.0-Windows-AMD64.zip`

### Advanced Windows Build

#### Custom Icon

1. Place your icon file at `assets/icon.ico`
2. Run the build script (it will automatically detect it)

#### Code Signing (Optional)

To sign your executable:

```cmd
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 "dist/GUI-Device-Tree-Generator.exe"
```

#### Installer Creation

Use Inno Setup to create an installer:

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Create `installer.iss`:

```ini
[Setup]
AppName=GUI Device Tree Generator
AppVersion=1.0.0
DefaultDirName={pf}\GUI Device Tree Generator
OutputBaseFilename=GUI-DTGen-Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\GUI-Device-Tree-Generator.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\GUI Device Tree Generator"; Filename: "{app}\GUI-Device-Tree-Generator.exe"
```

3. Compile with Inno Setup

## Linux Compilation

### Step 1: Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev python3-pip
sudo apt-get install cpio lz4 device-tree-compiler

# Fedora
sudo dnf install python3-devel python3-pip
sudo dnf install cpio lz4 dtc

# Arch Linux
sudo pacman -S python python-pip
sudo pacman -S cpio lz4 dtc
```

### Step 2: Prepare Environment

```bash
cd GUI-Device-Tree-Generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
```

### Step 3: Build Executable

```bash
python build_exe.py
```

Output: `dist/GUI-Device-Tree-Generator`

### Step 4: Test Executable

```bash
cd dist
./GUI-Device-Tree-Generator
```

### Step 5: Create Distribution Package

```bash
python build_exe.py --package
```

Output: `dist/GUI-Device-Tree-Generator-v1.0.0-Linux-x86_64.tar.gz`

### Creating AppImage (Recommended for Linux)

1. **Install appimagetool**:
   ```bash
   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
   chmod +x appimagetool-x86_64.AppImage
   ```

2. **Create AppDir structure**:
   ```bash
   mkdir -p AppDir/usr/bin
   mkdir -p AppDir/usr/share/applications
   mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps
   ```

3. **Copy files**:
   ```bash
   cp dist/GUI-Device-Tree-Generator AppDir/usr/bin/
   ```

4. **Create desktop entry** (`AppDir/usr/share/applications/dtgen.desktop`):
   ```ini
   [Desktop Entry]
   Type=Application
   Name=GUI Device Tree Generator
   Exec=GUI-Device-Tree-Generator
   Icon=dtgen
   Categories=Development;
   ```

5. **Build AppImage**:
   ```bash
   ./appimagetool-x86_64.AppImage AppDir GUI-Device-Tree-Generator-v1.0.0-x86_64.AppImage
   ```

## macOS Compilation

### Step 1: Install Homebrew Dependencies

```bash
brew install python3 cpio lz4 dtc
```

### Step 2: Prepare Environment

```bash
cd GUI-Device-Tree-Generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
```

### Step 3: Build Application Bundle

```bash
python build_exe.py --platform macos
```

Output: `dist/GUI-Device-Tree-Generator.app`

### Step 4: Test Application

```bash
open dist/GUI-Device-Tree-Generator.app
```

### Step 5: Create DMG (Disk Image)

```bash
# Create DMG for distribution
hdiutil create -volname "GUI Device Tree Generator" -srcfolder dist/GUI-Device-Tree-Generator.app -ov -format UDZO dist/GUI-Device-Tree-Generator-v1.0.0-macOS.dmg
```

### Code Signing (macOS)

To sign your app for distribution:

```bash
# Sign the application
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/GUI-Device-Tree-Generator.app

# Verify signature
codesign --verify --deep --strict --verbose=2 dist/GUI-Device-Tree-Generator.app

# Notarize with Apple (requires Apple Developer account)
xcrun notarytool submit dist/GUI-Device-Tree-Generator-v1.0.0-macOS.dmg --apple-id your@email.com --team-id TEAMID --password app-specific-password
```

## Advanced Configuration

### Customizing PyInstaller Spec File

For advanced customization, generate a spec file:

```bash
pyi-makespec --name="GUI-Device-Tree-Generator" --onefile --windowed src/main.py
```

Edit `GUI-Device-Tree-Generator.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/gui', 'gui'),
        ('src/core', 'core'),
        ('src/utils', 'utils'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL._tkinter_finder',
        'twrpdtgen',
        'psutil',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GUI-Device-Tree-Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
```

Build from spec:

```bash
pyinstaller GUI-Device-Tree-Generator.spec
```

### Reducing Executable Size

1. **Use UPX compression**:
   ```bash
   # Install UPX
   # Windows: Download from https://upx.github.io/
   # Linux: sudo apt-get install upx
   # macOS: brew install upx
   
   # PyInstaller will use UPX automatically if available
   ```

2. **Exclude unused modules**:
   Edit the spec file and add to `excludes`:
   ```python
   excludes=['unittest', 'email', 'html', 'xml', 'pydoc'],
   ```

3. **Strip debug symbols** (Linux/macOS):
   ```bash
   strip dist/GUI-Device-Tree-Generator
   ```

### Multi-Platform Build Script

Create `build_all.sh` for automated builds:

```bash
#!/bin/bash

set -e

echo "Building for all platforms..."

# Windows (on Windows or with Wine)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Building Windows executable..."
    python build_exe.py --package
fi

# Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Building Linux executable..."
    python build_exe.py --package
fi

# macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Building macOS application..."
    python build_exe.py --platform macos --package
fi

echo "Build complete! Check dist/ directory."
```

## Troubleshooting

### Issue: "ModuleNotFoundError" during execution

**Solution**: Add missing module to hidden imports:

```bash
pyinstaller --hidden-import=missing_module src/main.py
```

### Issue: Executable is too large (>100MB)

**Solutions**:
1. Use UPX compression
2. Exclude unused modules
3. Use `--onefile` instead of `--onedir`
4. Consider using a virtual environment with minimal packages

### Issue: "Failed to execute script" on Windows

**Solution**: Build in console mode first to see errors:

```bash
pyinstaller --console --onefile src/main.py
```

### Issue: Application won't start on other machines

**Possible causes**:
1. Missing Visual C++ Redistributable (Windows)
   - Include vcredist in installer
2. Missing system libraries (Linux)
   - Build on oldest supported system
   - Or use Docker for reproducible builds
3. Gatekeeper issues (macOS)
   - Sign and notarize the app
   - Or users can bypass: Right-click → Open

### Issue: CustomTkinter themes not working

**Solution**: Ensure theme files are included:

```python
# In spec file
datas=[
    ('venv/Lib/site-packages/customtkinter', 'customtkinter'),
],
```

### Docker Build (Reproducible Builds)

For consistent builds across environments:

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    cpio lz4 device-tree-compiler \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt pyinstaller
RUN python build_exe.py

CMD ["dist/GUI-Device-Tree-Generator"]
```

Build:
```bash
docker build -t dtgen-builder .
docker run --rm -v $(pwd)/dist:/app/dist dtgen-builder
```

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          pip install -r requirements.txt pyinstaller
          python build_exe.py --package
      - uses: actions/upload-artifact@v3
        with:
          name: windows-build
          path: dist/*.zip

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          sudo apt-get install -y cpio lz4 device-tree-compiler
          pip install -r requirements.txt pyinstaller
          python build_exe.py --package
      - uses: actions/upload-artifact@v3
        with:
          name: linux-build
          path: dist/*.tar.gz

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          brew install cpio lz4 dtc
          pip install -r requirements.txt pyinstaller
          python build_exe.py --platform macos --package
      - uses: actions/upload-artifact@v3
        with:
          name: macos-build
          path: dist/*.dmg
```

---

## Summary

You now have everything you need to compile the GUI Device Tree Generator for any platform. The resulting executables can be distributed to users who don't have Python installed.

**Quick Commands:**

```bash
# Windows
python build_exe.py --package

# Linux
python build_exe.py --package

# macOS
python build_exe.py --platform macos --package
```

For questions or issues, please visit the [GitHub repository](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator).
