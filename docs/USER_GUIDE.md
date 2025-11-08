# GUI Device Tree Generator - User Guide

Welcome to the comprehensive user guide for the GUI Device Tree Generator. This guide will walk you through installation, usage, and troubleshooting.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Using the Application](#using-the-application)
4. [Understanding the Output](#understanding-the-output)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)
7. [FAQ](#faq)

## Installation

### Windows Users

#### Option 1: Standalone Executable (Recommended)

1. Download the latest release from the [Releases page](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/releases)
2. Extract the ZIP file to a folder
3. Run `GUI-Device-Tree-Generator.exe`
4. That's it! No Python installation required.

#### Option 2: From Source

**Prerequisites:**
- Python 3.9 or higher
- Git (optional, for cloning)

**Steps:**

```bash
# Clone the repository
git clone https://github.com/himanshuksr0007/GUI-Device-Tree-Generator.git
cd GUI-Device-Tree-Generator

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### Linux Users

**Prerequisites:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk git
sudo apt-get install cpio lz4 device-tree-compiler abootimg

# Fedora
sudo dnf install python3 python3-pip python3-tkinter git
sudo dnf install cpio lz4 dtc abootimg

# Arch Linux
sudo pacman -S python python-pip tk git
sudo pacman -S cpio lz4 dtc abootimg
```

**Installation:**

```bash
# Clone repository
git clone https://github.com/himanshuksr0007/GUI-Device-Tree-Generator.git
cd GUI-Device-Tree-Generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

### macOS Users

**Prerequisites:**

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 git cpio lz4 dtc
```

**Installation:**

```bash
# Clone repository
git clone https://github.com/himanshuksr0007/GUI-Device-Tree-Generator.git
cd GUI-Device-Tree-Generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

## Getting Started

### First Launch

When you first launch the application:

1. The main window will appear with a modern dark theme
2. You'll see sections for:
   - Boot Image Selection
   - Configuration Options
   - Action Buttons
   - Progress Tracking
   - Generation Log

### System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB free space
- **OS**: Windows 10+, Ubuntu 20.04+, macOS 10.15+
- **Internet**: Required for initial setup (installing twrpdtgen)

## Using the Application

### Step 1: Select Boot Image

**Method 1: File Browser**
1. Click the "Select Image" button
2. Navigate to your boot.img or recovery.img file
3. Select the file and click "Open"

**Method 2: Drag and Drop**
1. Drag your boot.img or recovery.img file
2. Drop it onto the designated drop zone
3. The file will be automatically validated

**Supported Formats:**
- `.img` - Raw boot/recovery images
- `.tar` - TAR archives containing boot images
- `.gz` - GZip compressed images
- `.lz4` - LZ4 compressed images

**File Size Limits:**
- Minimum: 1 MB
- Maximum: 500 MB

### Step 2: Configure Options

#### Output Directory
- **Default**: `./output` (in the application directory)
- **Custom**: Click "Browse" to select a different location
- The generated device tree will be saved here

#### Device Tree Type
- **TWRP**: Generates TWRP-compatible device tree (Currently supported)
- **LineageOS**: Coming in future updates

For now, keep this set to "TWRP".

#### Additional Options

**Initialize Git Repository**
- ✅ Enabled (Recommended): Creates a git repository with initial commit
- ❌ Disabled: Just generates files without git

Benefit: Makes it easy to track changes and push to GitHub later.

**Validate Generated Device Tree**
- ✅ Enabled (Recommended): Checks for missing files and common issues
- ❌ Disabled: Skips validation

Benefit: Catches potential problems before you try to build.

### Step 3: Generate Device Tree

1. Click the **"🚀 Generate Device Tree"** button
2. Watch the progress bar and log for real-time updates
3. The process typically takes 1-5 minutes depending on:
   - Image size
   - Your system performance
   - Complexity of the device

### Step 4: Review Output

Once generation completes:

1. A success dialog will appear showing the output location
2. Navigate to the output directory
3. You'll find a folder structure like:

```
output/
└── manufacturer/
    └── codename/
        ├── Android.mk
        ├── AndroidProducts.mk
        ├── BoardConfig.mk
        ├── device.mk
        ├── omni_codename.mk
        ├── recovery.fstab
        ├── vendorsetup.sh
        └── recovery/
            └── root/
```

## Understanding the Output

### Key Files Explained

#### BoardConfig.mk
Contains hardware-specific build flags:
- Target architecture (ARM, ARM64, x86)
- Kernel configuration
- Partition sizes
- Recovery-specific settings

#### Android.mk
Main build entry point that tells the Android build system about your device.

#### AndroidProducts.mk
Defines the lunch targets for building your device.

#### device.mk
Specifies device-specific packages, properties, and configurations.

#### omni_codename.mk / twrp_codename.mk
ROM-specific makefile (depends on tree type).

#### recovery.fstab
Defines partition mount points for recovery mode.

#### vendorsetup.sh
Shell script that adds your device to the lunch menu.

### Using the Generated Tree

**For TWRP Building:**

```bash
# Copy to TWRP source
cp -r output/manufacturer/codename device/manufacturer/codename

# Setup environment
source build/envsetup.sh

# Select device
lunch omni_codename-eng

# Build TWRP
mka recoveryimage
```

**For LineageOS Building** (When supported):

```bash
# Copy to LineageOS source
cp -r output/manufacturer/codename device/manufacturer/codename

# Setup environment
source build/envsetup.sh

# Select device
lunch lineage_codename-userdebug

# Build ROM
mka bacon
```

## Troubleshooting

### Common Issues

#### Issue 1: "Failed to extract boot image"

**Possible Causes:**
- Corrupted image file
- Unsupported image format
- Insufficient permissions

**Solutions:**
1. Verify the image file isn't corrupted
2. Try using recovery.img instead of boot.img
3. Run the application as administrator (Windows) or with sudo (Linux)
4. Check that the file is actually a boot/recovery image

#### Issue 2: "twrpdtgen not installed"

**Solution:**
```bash
# Install twrpdtgen
pip install twrpdtgen

# Verify installation
python -m twrpdtgen --version
```

#### Issue 3: "Cannot detect device information"

**Possible Causes:**
- Image doesn't contain build.prop
- Custom/modified boot image
- Vendor image instead of boot image

**Solutions:**
1. Use recovery.img instead of boot.img (recovery usually has build.prop)
2. Extract build.prop from your device and place it in the image
3. Manually edit the generated files with correct information

#### Issue 4: "Generated device tree doesn't compile"

**This is normal!** Device trees often need manual adjustments:

1. Check the generation log for warnings
2. Review BoardConfig.mk for device-specific flags
3. Adjust partition sizes if needed
4. Add vendor blobs (see extracting vendor blobs section)
5. Test build and fix errors iteratively

#### Issue 5: Application won't start

**Windows:**
```bash
# Check if Python is installed
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Linux/macOS:**
```bash
# Check Python version
python3 --version

# Check if required packages are installed
which cpio lz4 dtc

# Reinstall system packages if missing
```

### Getting More Help

1. **Check the Log**: Review the generation log in the application for detailed error messages
2. **Check Log Files**: Look in the `logs/` directory for detailed log files
3. **GitHub Issues**: [Report an issue](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/issues)
4. **XDA Thread**: [Community support thread](https://xdaforums.com/) (Coming soon)

## Advanced Usage

### Command Line Usage

You can also use the core library programmatically:

```python
from src.core.processor import DeviceTreeProcessor

processor = DeviceTreeProcessor()

result = processor.process_image(
    image_path="path/to/boot.img",
    output_dir="output/",
    tree_type="twrp",
    init_git=True,
    validate=True
)

if result['success']:
    print(f"Device tree generated: {result['output_path']}")
    print(f"Device: {result['device_name']}")
else:
    print(f"Error: {result['error']}")
```

### Batch Processing

To process multiple images:

```python
images = [
    "device1_boot.img",
    "device2_recovery.img",
    "device3_boot.img"
]

for image in images:
    processor = DeviceTreeProcessor()
    result = processor.process_image(
        image_path=image,
        output_dir=f"output/{Path(image).stem}"
    )
    print(f"{image}: {'Success' if result['success'] else 'Failed'}")
```

### Customizing Output

After generation, you may want to customize:

1. **Add Custom Flags**: Edit `BoardConfig.mk`
2. **Add Custom Properties**: Edit `device.mk` or `system.prop`
3. **Modify Recovery Config**: Edit recovery-specific files
4. **Add Vendor Blobs**: Create `proprietary-files.txt`

### Extracting Vendor Blobs

The device tree generator creates the structure, but you'll need to extract vendor blobs:

```bash
# From a running device (ADB)
adb root
adb pull /vendor ./vendor_dump
adb pull /system/vendor ./vendor_dump

# Create proprietary-files.txt
# List all vendor files needed

# Use extract-files.sh (generated)
./extract-files.sh
```

## FAQ

### Q: Do I need to know programming to use this tool?
**A:** No! The GUI is designed for users of all skill levels. However, understanding device trees helps when customizing the output.

### Q: Will the generated device tree work immediately?
**A:** Usually not. Device trees typically need manual adjustments for:
- Device-specific kernel flags
- Partition configurations
- Recovery features
- Vendor blob paths

This tool gives you a solid starting point.

### Q: Can I use this for any Android device?
**A:** Yes, as long as you have the boot.img or recovery.img from your device. However, older devices (Android < 4.4) might have limited support.

### Q: Why TWRP only? When will LineageOS support come?
**A:** TWRP device trees are simpler and more standardized. LineageOS support is planned for version 1.1.

### Q: The tool says my image is invalid but it works on my device. Why?
**A:** Some manufacturer-specific image formats aren't recognized by the validator. If you're sure it's valid, you can:
1. Try using recovery.img instead
2. Report the issue on GitHub with image details

### Q: Can I contribute to this project?
**A:** Absolutely! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Q: Is this tool safe? Will it modify my device?
**A:** This tool only **reads** image files and **generates** device tree files. It never touches your actual device. It's completely safe.

### Q: Can I use the generated device tree commercially?
**A:** Yes! This tool is MIT licensed. You can use the output for any purpose, including commercial projects.

---

## Need More Help?

- **Documentation**: [Full Documentation](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/wiki)
- **Issues**: [GitHub Issues](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/discussions)

**Happy Device Tree Generating! 🚀**
