# GUI Device Tree Generator

A modern, user-friendly graphical interface for generating Android device trees from boot/recovery images. Built for ROM developers who want the power of automated device tree generation with an intuitive visual workflow.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## Features

### Core Functionality
- **Automated Device Tree Generation**: Extract hardware information and generate complete device trees from boot/recovery images
- **Modern GUI Interface**: Clean, intuitive interface built with CustomTkinter
- **Real-time Progress Tracking**: Visual feedback for all processing stages
- **Comprehensive Error Handling**: Clear, actionable error messages with suggested fixes
- **Multi-format Support**: Handles various boot image formats and compression methods
- **Cross-platform**: Works on Windows, Linux, and macOS

### Technical Capabilities
- Automatic device information extraction (codename, manufacturer, model, architecture)
- Kernel configuration parsing and analysis
- Partition scheme detection (A/B, dynamic partitions, SAR/non-SAR)
- Recovery fstab generation
- BoardConfig.mk generation with proper flags and parameters
- Android.mk and device.mk file generation
- Vendor blob list creation
- Git repository initialization (optional)

## Prerequisites

### System Requirements
- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space
- Internet connection (for initial setup)

### Platform-Specific Dependencies

**Windows:**
- Windows 10 or later (Windows 11 recommended)
- No additional dependencies required (bundled in executable)

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-tk cpio lz4 device-tree-compiler abootimg
```

**macOS:**
```bash
brew install python3 cpio lz4 dtc
```

## Installation

### Option 1: Pre-built Executable (Windows)
1. Download the latest release from [Releases](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/releases)
2. Extract the ZIP file
3. Run `GUI-Device-Tree-Generator.exe`

### Option 2: From Source
```bash
# Clone the repository
git clone https://github.com/himanshuksr0007/GUI-Device-Tree-Generator.git
cd GUI-Device-Tree-Generator

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

## Quick Start Guide

1. **Launch the Application**
   - Run the executable or `python src/main.py`

2. **Select Boot Image**
   - Click "Select Boot Image" or drag-and-drop your boot.img/recovery.img file
   - Supported formats: IMG, TAR, LZ4, GZ

3. **Configure Options**
   - Choose output directory
   - Select device tree type (TWRP/LineageOS)
   - Enable/disable optional features

4. **Generate Device Tree**
   - Click "Generate Device Tree"
   - Monitor progress in real-time
   - Review generated files in output directory

5. **Verify Output**
   - Check the generated device tree structure
   - Review the log for any warnings or recommendations
   - Test the device tree in your ROM build environment

## Project Structure

```
GUI-Device-Tree-Generator/
├── src/                        # Source code
│   ├── main.py                # Application entry point
│   ├── gui/                   # GUI components
│   │   ├── main_window.py    # Main application window
│   │   └── components.py     # Reusable UI components
│   ├── core/                  # Core processing logic
│   │   ├── processor.py      # Boot image processing
│   │   └── validator.py      # Validation and checks
│   └── utils/                 # Utility functions
│       └── logger.py         # Logging system
├── docs/                      # Documentation
│   ├── USER_GUIDE.md         # Detailed user guide
│   └── COMPILATION.md        # Build instructions
├── requirements.txt           # Python dependencies
├── setup.py                  # Package configuration
├── build_exe.py              # Executable build script
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## Building Executable

### Windows Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_exe.py

# Output: dist/GUI-Device-Tree-Generator.exe
```

### Linux AppImage
```bash
# Install dependencies
pip install pyinstaller

# Build executable
python build_exe.py --platform linux

# Output: dist/GUI-Device-Tree-Generator
```

### macOS App Bundle
```bash
# Install dependencies
pip install pyinstaller

# Build application
python build_exe.py --platform macos

# Output: dist/GUI-Device-Tree-Generator.app
```

## Usage Examples

### Basic TWRP Device Tree Generation
```python
# Using the GUI is recommended, but you can also use the core library
from src.core.processor import DeviceTreeProcessor

processor = DeviceTreeProcessor()
result = processor.process_boot_image(
    image_path="path/to/boot.img",
    output_dir="output/",
    tree_type="twrp"
)
```

## Troubleshooting

### Common Issues

**Issue: "Failed to extract boot image"**
- Ensure the image file is not corrupted
- Verify the file is a valid boot/recovery image
- Check file permissions

**Issue: "Cannot detect device information"**
- The boot image may lack build.prop
- Try using a recovery image instead
- Manually specify device details

**Issue: "Generated device tree doesn't compile"**
- Review the generation log for warnings
- Some devices require manual BoardConfig.mk adjustments
- Check for missing vendor blobs

See [docs/USER_GUIDE.md](docs/USER_GUIDE.md) for detailed troubleshooting.

## Contributing

Contributions are welcome! Please read our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/GUI-Device-Tree-Generator.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run with debugging
python src/main.py --debug
```

## Roadmap

### Version 1.0 (Current)
- ✅ TWRP device tree generation
- ✅ Modern GUI interface
- ✅ Cross-platform support
- ✅ Real-time progress tracking

### Version 1.1 (Planned)
- LineageOS/AOSP device tree support
- Batch processing multiple images
- Device tree comparison tool
- Template customization

### Version 2.0 (Future)
- Full ROM dump support (aospdtgen integration)
- GitHub integration (direct push)
- Built-in device tree editor
- Community template library

## Technology Stack

- **GUI Framework**: CustomTkinter (modern Tkinter themes)
- **Backend Engine**: twrpdtgen (proven device tree generator)
- **Image Processing**: Android Image Kitchen integration
- **Build System**: PyInstaller (cross-platform executables)
- **Testing**: pytest (comprehensive test suite)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [twrpdtgen](https://github.com/twrpdtgen/twrpdtgen) - Core device tree generation engine
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework
- Android ROM development community for inspiration and feedback
- All contributors who have helped improve this tool

## Support

- **Issues**: [GitHub Issues](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/discussions)
- **XDA Thread**: [Coming Soon]

## Author

**Himanshu Kumar**
- GitHub: [@himanshuksr0007](https://github.com/himanshuksr0007)
- Created with ❤️ for the Android ROM development community

---

**Star this repository if you find it useful! ⭐**
