#!/usr/bin/env python
"""
Manual Virtual Environment Setup for DS101
A simpler, more relia        print("\n🌍 Downloading GeoNames database...")
        print("📊 This downloads ~1GB of geographic data and may take some time")
        print("📺 You will see the download progress below:") approach that ensures VS Code recognition
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

def setup_roberta_model_in_venv(venv_python):
    """Pre-download RoBERTa model to avoid classroom delays."""
    print("\n🤖 Pre-downloading RoBERTa sentiment model...")
    print("📊 This downloads ~500MB and prevents delays during class")
    print("📺 You will see the download progress below:")
    
    roberta_script = '''
import os
import sys

try:
    print("🔄 Loading RoBERTa model (this may take a few minutes)...")
    
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    
    # Download and cache the model components
    print("📥 Downloading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    
    print("📥 Downloading model...")
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    
    print("✅ RoBERTa model downloaded and cached successfully!")
    print("💡 Model files are now available for instant loading during lessons")
    
except ImportError as e:
    print(f"⚠️ Transformers library not available: {e}")
    print("This is OK - RoBERTa will download when first used")
    sys.exit(0)
except Exception as e:
    print(f"⚠️ Could not pre-download RoBERTa model: {e}")
    print("This is OK - model will download when first used in lessons")
    sys.exit(0)
'''
    
    try:
        # Use a longer timeout for model download
        subprocess.check_call([venv_python, "-c", roberta_script], timeout=900)  # 15 minutes max
        return True
    except subprocess.TimeoutExpired:
        print("⚠️ RoBERTa download timeout - model will download during lessons")
        return False
    except subprocess.CalledProcessError as e:
        print(f"⚠️ RoBERTa pre-download failed: {e}")
        print("This is OK - model will download when first used")
        return False

def setup_spacy_models_in_venv(venv_python):
    """Download required spaCy language models using venv python."""
    print("🤖 Setting up spaCy models...")
    
    models = ["en_core_web_sm", "en_core_web_md", "en_core_web_trf"]
    for model_name in models:
        try:
            print(f"📥 Downloading spaCy model: {model_name}...")
            subprocess.check_call([venv_python, "-m", "spacy", "download", model_name])
            print(f"✅ {model_name} downloaded successfully")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to download {model_name}")

def setup_geoparser_in_venv(venv_python):
    """Setup geoparser and download GeoNames database using venv python."""
    print("\n🌍 Setting up geoparser...")
    
    # First check if geoparser is even installed
    try:
        subprocess.run([venv_python, "-c", "import geoparser"], 
                      check=True, capture_output=True)
        print("✅ Geoparser package is installed")
    except subprocess.CalledProcessError:
        print("❌ Geoparser not installed - this should have been installed in the previous step")
        print("💡 Try running the script again or install manually: pip install geoparser")
        return False
    
    # Check if GeoNames data is already downloaded
    print("🔍 Checking for existing GeoNames database...")
    try:
        result = subprocess.run([venv_python, "-c", 
                               "import geoparser; gn = geoparser.GeoNames(); print('Data available' if gn.data_dir.exists() else 'No data')"],
                              capture_output=True, text=True)
        if "Data available" in result.stdout:
            print("✅ GeoNames database already available")
            return True
        else:
            print("📥 GeoNames database not found, downloading...")
    except subprocess.CalledProcessError:
        print("📥 Could not verify existing data, proceeding with download...")
    
    try:
        print("\n🌍 Downloading GeoNames database...")
        print("� This downloads ~1GB of geographic data and may take 10-15 minutes")
        print("📺 You will see the download progress below:")
        print(f"🔧 Command: {venv_python} -m geoparser download geonames")
        print("-" * 60)
        
        # Show real-time output by not capturing it
        result = subprocess.run([venv_python, "-m", "geoparser", "download", "geonames"])
        
        print("-" * 60)
        if result.returncode == 0:
            print("✅ GeoNames database downloaded successfully")
            return True
        else:
            print(f"❌ Geoparser download failed with return code {result.returncode}")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to download GeoNames database: {e}")
        print("💡 You can try again later by running:")
        print(f"   {venv_python} -m geoparser download geonames")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Download cancelled by user")
        print("💡 You can resume later by running:")
        print(f"   {venv_python} -m geoparser download geonames")
        return False

def check_packages_installed(python_exe, packages):
    """Check if required packages are installed in the environment."""
    print("🔍 Checking existing packages...")
    missing_packages = []
    
    for package in packages:
        try:
            subprocess.run([python_exe, "-c", f"import {package.replace('-', '_')}"], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} is installed")
        except subprocess.CalledProcessError:
            missing_packages.append(package)
            print(f"   ❌ {package} is missing")
        except Exception:
            # For packages with different import names, just try pip show
            try:
                result = subprocess.run([python_exe, "-m", "pip", "show", package], 
                                      check=True, capture_output=True)
                if result.returncode == 0:
                    print(f"   ✅ {package} is installed")
                else:
                    missing_packages.append(package)
                    print(f"   ❌ {package} is missing")
            except:
                missing_packages.append(package)
                print(f"   ❌ {package} is missing")
    
    return missing_packages

def main():
    print("Manual DS101 Environment Setup")
    print("=" * 40)
    
    # Get current directory
    current_dir = os.getcwd()
    venv_name = "ds101_manual"
    venv_path = os.path.join(current_dir, venv_name)
    
    print(f"Checking virtual environment at: {venv_path}")
    
    # Step 1: Check if environment exists
    env_exists = os.path.exists(venv_path)
    
    if env_exists:
        print("✅ Virtual environment already exists")
        
        # Get Python executable path for existing environment
        if platform.system() == "Windows":
            python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            python_candidate = os.path.join(venv_path, "bin", "python")
            python3_candidate = os.path.join(venv_path, "bin", "python3")
            
            if platform.system() == "Darwin":  # macOS
                python_exe = python3_candidate if os.path.exists(python3_candidate) else python_candidate
            else:  # Linux/Ubuntu
                python_exe = python_candidate if os.path.exists(python_candidate) else python3_candidate
        
        # Check if Python executable exists and works
        try:
            subprocess.run([python_exe, "--version"], check=True, capture_output=True)
            print(f"✅ Python executable working: {python_exe}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Python executable not working, recreating environment...")
            env_exists = False
    
    if not env_exists:
        # Remove existing broken environment if it exists
        if os.path.exists(venv_path):
            print("🗑️ Removing broken environment...")
            import shutil
            shutil.rmtree(venv_path)
        
        # Step 2: Create virtual environment
        print("📦 Creating new virtual environment...")
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
    
    # Check which packages are missing
    if env_exists:
        missing_packages = check_packages_installed(python_exe, packages)
        if not missing_packages:
            print("✅ All required packages are already installed!")
        else:
            print(f"📦 Installing {len(missing_packages)} missing packages...")
            packages_to_install = missing_packages
    else:
        print("📦 Installing all packages in new environment...")
        packages_to_install = packages
    
    # Install only missing packages with real-time output
    for package in packages_to_install:
        print(f"\n📦 Installing {package}...")
        print(f"   Command: {python_exe} -m pip install {package}")
        
        try:
            # Show real-time output by not capturing it
            result = subprocess.run([python_exe, "-m", "pip", "install", package], 
                                  check=True)
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}")
            print(f"💡 You may need to install this manually: {python_exe} -m pip install {package}")
            print(f"Error details: {e}")
    
    # Step 5: Register Jupyter kernel
    kernel_name = "ds101-manual"
    display_name = "Python 3 (DS101 Manual)"
    
    # Check if kernel already exists
    try:
        result = subprocess.run([python_exe, "-m", "jupyter", "kernelspec", "list"], 
                              capture_output=True, text=True)
        if kernel_name in result.stdout:
            print(f"✅ Jupyter kernel '{display_name}' already exists")
        else:
            print(f"🔧 Registering Jupyter kernel: {display_name}")
            subprocess.run([
                python_exe, "-m", "ipykernel", "install",
                "--user",
                "--name", kernel_name,
                "--display-name", display_name
            ], check=True, capture_output=True)
            print("✅ Kernel registered successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Could not check/register kernel (this is usually OK): {e}")
        # Try to register anyway
        try:
            subprocess.run([
                python_exe, "-m", "ipykernel", "install",
                "--user",
                "--name", kernel_name,
                "--display-name", display_name
            ], check=True, capture_output=True)
            print("✅ Kernel registered successfully")
        except subprocess.CalledProcessError as e2:
            print(f"❌ Failed to register kernel: {e2}")
    
    # Step 5.5: Setup NLP resources
    print("\n📚 Setting up NLP resources...")
    setup_nltk_data_in_venv(python_exe)
    setup_spacy_models_in_venv(python_exe)
    setup_geoparser_in_venv(python_exe)
    
    # Step 5.6: Pre-download RoBERTa model for sentiment analysis
    setup_roberta_model_in_venv(python_exe)
    
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