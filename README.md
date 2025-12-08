# MikesToolsLibrary 🔧

A Python library designed to provide expressive, maintainable logging systems with custom Unicode symbols, color schemes, and extensible formatter logic. Built for clarity, reproducibility, and developer experience.

---

## ✨ Features
- ✅ Custom log levels (TRACE, DATA, SUCCESS, CONFIG, SECURITY)
- 🎨 Unicode symbols and color-coded console output
- 🧪 Automated testing with pytest
- 📦 PyPI-ready packaging with clean module layout
- 🔒 Security-conscious handler mappings and error signaling
- 🛠 Extensible architecture for future-proof workflows

---

## 📦 Installation
Install directly from PyPI (once published):

```bash
pip install MikesToolsLibrary



git clone https://github.com/lostwizz/MikesToolsLibrary.git
cd MikesToolsLibrary
pip install -e .

---

## Useage Examples
from mikestoolslibrary import logger

- logger.trace("Tracing execution flow...")
- logger.data("Logging structured data")
- logger.success("Operation completed successfully!")
- logger.config("Configuration loaded")
- logger.security("Security check passed")