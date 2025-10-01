#!/usr/bin/env python
"""
Manual Virtual Environment Setup for DS101
A simpler, more reliable approach that ensures VS Code recognition
"""

import os
import sys
import subprocess
import venv
import json
import platform

def setup_nltk_data_in_venv(venv_python):
    """Download required NLTK data packages using venv python."""
    print("📚 Setting up NLTK data...")
    
    nltk_script = '''
import nltk
import ssl

# Handle SSL certificate issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
packages = [("punkt", "tokenizers/punkt"), ("vader_lexicon", "vader_lexicon")]
for package, path in packages:
    try:
        nltk.data.find(path)
        print(f"✅ NLTK {package} already available")
    except LookupError:
        print(f"📥 Downloading NLTK {package}...")
        nltk.download(package, quiet=True)
        print(f"✅ NLTK {package} downloaded successfully")
'''
    
    try:
        subprocess.check_call([venv_python, "-c", nltk_script])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup NLTK data: {e}")
        return False

def setup_spacy_models_in_venv(venv_python):
    """Download required spaCy language models using venv python."""
    print("🤖 Setting up spaCy models...")
    
    models = ["en_core_web_sm", "en_core_web_md"]
    for model_name in models:
        try:
            print(f"📥 Downloading spaCy model: {model_name}...")
            subprocess.check_call([venv_python, "-m", "spacy", "download", model_name])
            print(f"✅ {model_name} downloaded successfully")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to download {model_name}")

def setup_geoparser_in_venv(venv_python):
    """Setup geoparser and download GeoNames database using venv python."""
    print("🌍 Setting up geoparser...")
    
    try:
        print("📥 Downloading GeoNames database (this may take a while)...")
        print("💾 This will download ~1GB of geographic data")
        
        subprocess.check_call([venv_python, "-m", "geoparser", "download", "geonames"])
        print("✅ GeoNames database downloaded successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to setup geoparser: {e}")
        print("💡 You can set this up later by activating the environment and running: python -m geoparser download geonames")
        return False

def main():
    print("Manual DS101 Environment Setup")
    print("=" * 40)
    
    # Get current directory
    current_dir = os.getcwd()
    venv_name = "ds101_manual"
    venv_path = os.path.join(current_dir, venv_name)
    
    print(f"Creating virtual environment at: {venv_path}")
    
    # Step 1: Remove existing environment if it exists
    if os.path.exists(venv_path):
        print("Removing existing environment...")
        import shutil
        shutil.rmtree(venv_path)
    
    # Step 2: Create virtual environment
    print("Creating new virtual environment...")
    venv.create(venv_path, with_pip=True)
    
    # Step 3: Get Python executable path
    if platform.system() == "Windows":
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
    else:
        # Unix-like systems (Linux/Mac) - check for both python and python3
        python_candidate = os.path.join(venv_path, "bin", "python")
        python3_candidate = os.path.join(venv_path, "bin", "python3")
        
        # Platform-specific preference order
        if platform.system() == "Darwin":  # macOS
            # Mac prefers python3, fallback to python
            if os.path.exists(python3_candidate):
                python_exe = python3_candidate
            elif os.path.exists(python_candidate):
                python_exe = python_candidate
            else:
                python_exe = python3_candidate  # Fallback
        else:  # Linux/Ubuntu
            # Linux prefers python, fallback to python3
            if os.path.exists(python_candidate):
                python_exe = python_candidate
            elif os.path.exists(python3_candidate):
                python_exe = python3_candidate
            else:
                python_exe = python_candidate  # Fallback
        
        activate_script = os.path.join(venv_path, "bin", "activate")
    
    print(f"🐍 Python executable: {python_exe}")
    
    # Step 4: Install essential packages (complete list from simple_setup.py)
    packages = [
        # Essential Jupyter packages first
        "ipykernel",         # Required for Jupyter kernels
        "jupyter",
        "jupyterlab", 
        "ipywidgets",
        "notebook",
        
        # Basic data science stack
        "pandas",
        "numpy",
        
        
        # Interactive visualization
        "plotly",
        "mapclassify",
        
        # Progress bars
        "tqdm",
        
        # Reddit scraping (Lesson 1)
        "praw",
        
        # NLP packages (Lessons 4-5)
        "nltk",
        "spacy",
        "geoparser",
        
        # Machine Learning / Transformers (Lesson 5)
        "transformers",
        "torch",
        
        

        # Utilities
        "cryptography",
        "requests"
    ]
    
    print("📦 Installing packages...")
    for package in packages:
        print(f"   Installing {package}...")
        try:
            subprocess.run([python_exe, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
    
    # Step 5: Register Jupyter kernel
    kernel_name = "ds101-manual"
    display_name = "Python 3 (DS101 Manual)"
    
    print(f"🔧 Registering Jupyter kernel: {display_name}")
    try:
        subprocess.run([
            python_exe, "-m", "ipykernel", "install",
            "--user",
            "--name", kernel_name,
            "--display-name", display_name
        ], check=True, capture_output=True)
        print("✅ Kernel registered successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to register kernel: {e}")
        return
    
    # Step 5.5: Setup NLP resources
    print("\n📚 Setting up NLP resources...")
    setup_nltk_data_in_venv(python_exe)
    setup_spacy_models_in_venv(python_exe)
    setup_geoparser_in_venv(python_exe)
    
    # Step 6: Create VS Code settings
    print("⚙️  Creating VS Code settings...")
    
    # Create .vscode directory
    vscode_dir = ".vscode"
    os.makedirs(vscode_dir, exist_ok=True)
    
    # Create settings.json
    settings = {
        "python.defaultInterpreterPath": python_exe.replace("\\\\", "/"),
        "python.pythonPath": python_exe.replace("\\\\", "/"),
        "jupyter.kernels.filter": [
            {
                "path": python_exe.replace("\\\\", "/"),
                "type": "pythonEnvironment"
            }
        ],
        "jupyter.interactiveWindow.creationMode": "perFile"
    }
    
    settings_path = os.path.join(vscode_dir, "settings.json")
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=4)
    
    print(f"✅ VS Code settings created at: {settings_path}")
    
    # Step 7: Create activation batch file for Windows
    if platform.system() == "Windows":
        batch_content = f'''@echo off
echo Activating DS101 Environment...
call "{activate_script}"
echo  DS101 Environment activated!
echo  Python: {python_exe}
echo  To deactivate, type: deactivate
cmd /k
'''
        
        batch_path = "activate_ds101.bat"
        with open(batch_path, "w") as f:
            f.write(batch_content)
        
        print(f"✅ Created activation script: {batch_path}")
    
    # Final instructions
    print("\\n" + "=" * 50)
    print(" Manual Setup Complete!")
    print("=" * 50)
    
    print("\\n Next Steps:")
    print("1. **Restart VS Code completely**")
    print("2. Reopen this folder in VS Code")
    print("3. Open a .ipynb file")
    print("4. Click on the kernel selector (top right)")
    print(f"5. Look for: '{display_name}'")
    print("6. If not visible, click 'Select Another Kernel...'")
    print("7. Choose 'Python Environments'")
    print(f"8. Select the path: {python_exe}")
    
    print("\\n🔧 Alternative Method:")
    print("1. Press Ctrl+Shift+P")
    print("2. Type: 'Python: Select Interpreter'")
    print(f"3. Choose: {python_exe}")
    
    if platform.system() == "Windows":
        print("\\n Terminal Usage:")
        print(f"• Double-click: {batch_path}")
        print("• Or manually activate with:")
        print(f"  {activate_script}")
    
    print("\\n Environment Details:")
    print(f"• Name: {kernel_name}")
    print(f"• Path: {venv_path}")
    print(f"• Python: {python_exe}")
    print(f"• Kernel: {display_name}")

if __name__ == "__main__":
    main()