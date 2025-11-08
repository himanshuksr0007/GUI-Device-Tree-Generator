from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gui-device-tree-generator",
    version="1.0.0",
    author="Himanshu Kumar",
    author_email="83110103+himanshuksr0007@users.noreply.github.com",
    description="A modern GUI for generating Android device trees from boot/recovery images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/himanshuksr0007/GUI-Device-Tree-Generator",
    project_urls={
        "Bug Tracker": "https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/issues",
        "Documentation": "https://github.com/himanshuksr0007/GUI-Device-Tree-Generator/wiki",
        "Source Code": "https://github.com/himanshuksr0007/GUI-Device-Tree-Generator",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "customtkinter>=5.2.1",
        "Pillow>=10.1.0",
        "twrpdtgen>=1.3.0",
        "psutil>=5.9.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "build": [
            "pyinstaller>=6.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gui-dtgen=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="android device-tree rom twrp lineageos gui automation",
)
