# 🏷️ Label Generator

A desktop Python application designed to generate and export custom labels into printable PDF files with barcoding and a modern graphical interface.

---

## 🚀 Features

* 🎨 Modern and intuitive GUI built with **CustomTkinter**.
* 📄 Automatic PDF generation ready for printing.
* 📊 Support for multiple barcode standards (Code 39, Code 93, Code 128, etc.).
* 📦 Easy packaging into a standalone Windows executable (`.exe`).

---

## 🛠️ Prerequisites

Before you begin, make sure you have the following installed on your machine:
* **[Python 3.10+](https://www.python.org/downloads/)**
* **Git** (optional, to clone the repository)

> ⚠️ **Important:** During Python installation, make sure to check the box **"Add Python to PATH"**.

---

## 📥 Getting Started (For Developers)

### 1. Clone or Download the Repository

If you are using Git:
```bash
2. Create and Activate a Virtual Environment (Recommended)
In your terminal (PowerShell or CMD), navigate to the project directory:

PowerShell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# If execution policy blocks script execution in PowerShell, run this first:
# Set-ExecutionPolicy Unrestricted -Scope Process

3. Install Dependencies
With the virtual environment activated, install the required packages:

PowerShell
pip install customtkinter reportlab pillow pyinstaller

4. Run the Application
To start the application in development mode:

PowerShell
python main.py

⚙️ How to Build the Executable (.exe)
If you modify the source code and need to build a clean .exe binary without missing module errors:

Run the complete PyInstaller command:

PowerShell
python -m PyInstaller --onefile --windowed --collect-all customtkinter --collect-submodules reportlab.graphics.barcode main.py

📌 Command Flags Breakdown:
--onefile: Packages the entire application into a single executable file.

--windowed: Hides the command prompt window when opening the app.

--collect-all customtkinter: Embeds all UI themes, assets, and icons properly.

--collect-submodules reportlab.graphics.barcode: Bundles all ReportLab barcode submodules to prevent ModuleNotFoundError crashes.

The generated executable will be placed inside the dist/main.exe folder.

💻 For End Users (Running the Executable Only)
If you downloaded this repository just to run the application on Windows:

Open the dist/ folder.

Double-click main.exe (or LabelGenerator.exe).

The app will launch directly, with no Python installation required on your machine.

📁 Project Structure
Plaintext
📂 LabelGenerator/
├── 📄 main.py              # Application entry point
├── 📄 interface.py         # GUI code (CustomTkinter)
├── 📄 pdf.py               # PDF & Barcode generation logic (ReportLab)
├── 📁 dist/                # Output folder for compiled .exe
└── 📄 README.md            # Project documentation
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

git clone [https://github.com/gbmnagpng/Gerador-etiquetas-clientes.git](https://github.com/gbmnagpng/Gerador-etiquetas-clientes.git)
cd Gerador-etiquetas-clientes

