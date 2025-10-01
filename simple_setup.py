#!/usr/bin/env python3
"""
Digital Studies 101 - Ultra-Simple Setup
One command to rule them all!

This script creates a virtual environment and sets up everything students need 
for Jupyter in VS Code on macOS (with Homebrew Python) and Windows.

Works around Homebrew's "externally-managed-environment" restrictions.

Usage: python3 simple_setup.py
"""

import subprocess
import sys
import os
import json
import platform
import shutil
import venv

def run_command(cmd, description="Running command", check=True):
    """Run a command and show user-friendly output."""
    print(f"🔧 {description}...")
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error: {e}")
        return False
    except Exception as e:
        print(f"❌ {description} - Unexpected error: {e}")
        return False

def check_vscode_installed():
    """Check if VS Code is installed and accessible."""
    print("🔍 Checking for Visual Studio Code installation...")
    
    # Try different command names for VS Code
    vscode_commands = ['code', 'code-insiders']
    
    for cmd in vscode_commands:
        if shutil.which(cmd):
            # Test if the command actually works
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Found working VS Code command: {cmd}")
                    return cmd
                else:
                    print(f"⚠️  Found {cmd} but it's not working properly")
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                print(f"⚠️  Found {cmd} in PATH but it's not functional")
    
    # Platform-specific checks
    system = platform.system()
    if system == "Windows":
        print("🔍 Searching for VS Code in common Windows locations...")
        username = os.getenv('USERNAME', '')
        
        # More comprehensive list of possible VS Code locations
        possible_paths = [
            # Standard installation paths
            r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
            rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
            
            # Direct executable paths
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe", 
            rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            
            # Alternative installation locations
            r"C:\Program Files\Microsoft VS Code\code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\code.exe",
            rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\code.exe",
            
            # System-wide installations
            r"C:\Windows\System32\code.cmd",
            r"C:\Windows\System32\code.exe",
            
            # Portable installations (common locations)
            rf"C:\Users\{username}\Desktop\VSCode-win32-x64\Code.exe",
            rf"C:\Users\{username}\Downloads\VSCode-win32-x64\Code.exe",
            r"C:\VSCode\Code.exe",
            r"C:\PortableApps\VSCode\Code.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"🔍 Testing: {path}")
                try:
                    result = subprocess.run([path, "--version"], 
                                          capture_output=True, text=True, timeout=15)
                    if result.returncode == 0:
                        print(f"✅ Found working VS Code at: {path}")
                        return path
                    else:
                        print(f"⚠️  Found VS Code at {path} but version check failed")
                        print(f"    Return code: {result.returncode}")
                        if result.stderr:
                            print(f"    Error: {result.stderr.strip()[:100]}...")
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
                    print(f"⚠️  Could not execute {path}: {type(e).__name__}")
                    continue
        
        # Try to find VS Code using Windows Registry
        try:
            import winreg
            print("🔍 Checking Windows Registry for VS Code...")
            
            # Check common registry locations
            registry_paths = [
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]
            
            for hkey, reg_path in registry_paths:
                try:
                    with winreg.OpenKey(hkey, reg_path) as key:
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                if "visual studio code" in subkey_name.lower() or "vscode" in subkey_name.lower():
                                    with winreg.OpenKey(key, subkey_name) as subkey:
                                        try:
                                            install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                            code_path = os.path.join(install_location, "Code.exe")
                                            if os.path.exists(code_path):
                                                print(f"🔍 Found VS Code via registry: {code_path}")
                                                result = subprocess.run([code_path, "--version"], 
                                                                      capture_output=True, text=True, timeout=10)
                                                if result.returncode == 0:
                                                    print(f"✅ Registry VS Code works: {code_path}")
                                                    return code_path
                                        except FileNotFoundError:
                                            pass
                                i += 1
                            except OSError:
                                break
                except (OSError, FileNotFoundError):
                    continue
        except ImportError:
            print("⚠️  Could not import winreg for registry search")
    
    elif system == "Darwin":  # macOS
        print("🔍 Searching for VS Code on macOS...")
        vscode_path = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
        if os.path.exists(vscode_path):
            try:
                result = subprocess.run([vscode_path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Found working VS Code at: {vscode_path}")
                    return vscode_path
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                pass
    
    # Final fallback: ask user to provide VS Code path
    print("❌ Visual Studio Code not found automatically")
    print("💡 Since you're running this in VS Code, let's try to find it manually...")
    
    # Try some intelligent guesses based on common patterns
    print("� Trying intelligent search patterns...")
    import glob
    
    search_patterns = [
        r"C:\**\Microsoft VS Code\Code.exe",
        r"C:\Users\**\Microsoft VS Code\Code.exe", 
        rf"C:\Users\{os.getenv('USERNAME', '')}**\Code.exe",
        r"C:\Program Files*\**\Code.exe",
    ]
    
    for pattern in search_patterns:
        try:
            matches = glob.glob(pattern, recursive=True)
            for match in matches:
                if "Microsoft VS Code" in match or "VSCode" in match:
                    print(f"🔍 Testing found path: {match}")
                    try:
                        result = subprocess.run([match, "--version"], 
                                              capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            print(f"✅ Found working VS Code: {match}")
                            return match
                    except:
                        continue
        except:
            continue
    
    # If still not found, provide helpful guidance
    print("\n❌ Could not automatically locate VS Code")
    print("💡 You can either:")
    print("1. Skip VS Code extensions for now (they're not critical)")
    print("2. Install extensions manually later through VS Code's Extensions panel")
    print("3. Re-run this script after ensuring 'code' command works in terminal")
    print("\n🔧 To fix the 'code' command:")
    print("   • Open VS Code")
    print("   • Press Ctrl+Shift+P")
    print("   • Type: 'Shell Command: Install code command in PATH'")
    print("   • Select it and restart your terminal")
    
    return None

def install_vscode_extension(vscode_cmd, extension_id, extension_name):
    """Install a single VS Code extension."""
    try:
        print(f"📦 Installing {extension_name}...")
        result = subprocess.run([vscode_cmd, "--install-extension", extension_id], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {extension_name} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {extension_name}")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  {extension_name} installation timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error installing {extension_name}: {e}")
        return False

def setup_nltk_data():
    """Download required NLTK data packages."""
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
        subprocess.check_call([sys.executable, "-c", nltk_script])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup NLTK data: {e}")
        return False

def setup_spacy_models():
    """Download required spaCy language models."""
    print("🤖 Setting up spaCy models...")
    
    models = ["en_core_web_sm", "en_core_web_md"]
    for model_name in models:
        try:
            print(f"📥 Downloading spaCy model {model_name}...")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            print(f"✅ spaCy model {model_name} downloaded successfully")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to download spaCy model {model_name} - you can install it later")

def setup_geoparser():
    """Setup geoparser and download GeoNames database."""
    print("🌍 Setting up geoparser...")
    
    try:
        print("📥 Downloading GeoNames database (this may take a while)...")
        print("💾 This will download ~1GB of geographic data")
        
        subprocess.check_call([sys.executable, "-m", "geoparser", "download", "geonames"])
        print("✅ GeoNames database downloaded successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to setup geoparser: {e}")
        print("💡 You can set this up later with: python -m geoparser download geonames")
        return False

def create_virtual_environment(venv_path):
    """Create a virtual environment for the course."""
    print(f"🔧 Creating virtual environment at: {venv_path}")
    
    try:
        # Remove existing venv if it exists
        if os.path.exists(venv_path):
            print("🗑️  Removing existing virtual environment...")
            shutil.rmtree(venv_path)
        
        # Create new virtual environment
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_venv_python(venv_path):
    """Get the path to Python executable in the virtual environment."""
    system = platform.system()
    if system == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def install_package_in_venv(venv_python, package_name):
    """Install a package in the virtual environment."""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", package_name])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

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
            print(f"📥 Downloading spaCy model {model_name}...")
            subprocess.check_call([venv_python, "-m", "spacy", "download", model_name])
            print(f"✅ spaCy model {model_name} downloaded successfully")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to download spaCy model {model_name} - you can install it later")

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
        print(f"⚠️  Failed to setup geoparser: {e}")
        print("💡 You can set this up later by activating the environment and running: python -m geoparser download geonames")
        return False

def main():
    print("🚀 Digital Studies 101 - Ultra-Simple Setup")
    print("=" * 50)
    print("Setting up Jupyter + VS Code with virtual environment...")
    print("This works around Homebrew Python restrictions on macOS.")
    print("This will take 15-30 minutes.\n")

    # Determine paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_name = "ds101_env"
    venv_path = os.path.join(script_dir, venv_name)
    
    print(f"📁 Working directory: {script_dir}")
    print(f"📁 Virtual environment will be created at: {venv_path}")

    # Step 1: Create virtual environment
    print("\n🔧 Step 1: Creating virtual environment...")
    if not create_virtual_environment(venv_path):
        print("❌ Failed to create virtual environment")
        sys.exit(1)

    # Get venv python path
    venv_python = get_venv_python(venv_path)
    print(f"🐍 Using Python: {venv_python}")

    # Step 2: Upgrade pip in virtual environment
    print("\n🔄 Step 2: Upgrading pip in virtual environment...")
    run_command([venv_python, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")

    # Step 3: Install all required packages in virtual environment
    print("\n📦 Step 3: Installing Python packages in virtual environment...")
    
    # Complete package list from installs_required.py
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
        "matplotlib",
        "seaborn",
        
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
        "scipy",
        "scikit-learn",

        # Utilities
        "cryptography",
        "requests"
    ]
    
    failed_packages = []
    for package in packages:
        if not install_package_in_venv(venv_python, package):
            failed_packages.append(package)

    # Step 4: Register Jupyter kernel globally with proper configuration
    print("\n🔧 Step 4: Setting up Jupyter kernel...")
    kernel_name = "python3-ds101"
    display_name = "Python 3 (DS101)"
    
    # First, install the kernel
    if not run_command([
        venv_python, "-m", "ipykernel", "install", 
        "--user", 
        "--name", kernel_name,
        "--display-name", display_name
    ], "Registering Jupyter kernel"):
        print("❌ Failed to register Jupyter kernel")
        sys.exit(1)
    
    # Update the kernel.json with absolute paths for better persistence
    import os.path as path
    if platform.system() == "Windows":
        kernel_dir = path.expanduser(f"~\\AppData\\Roaming\\jupyter\\kernels\\{kernel_name}")
    else:
        kernel_dir = path.expanduser(f"~/.local/share/jupyter/kernels/{kernel_name}")
    
    kernel_json_path = path.join(kernel_dir, "kernel.json")
    if path.exists(kernel_json_path):
        try:
            # Read the existing kernel.json
            with open(kernel_json_path, 'r') as f:
                kernel_config = json.load(f)
            
            # Update with absolute paths
            kernel_config["argv"][0] = venv_python
            kernel_config["display_name"] = display_name
            kernel_config["language"] = "python"
            
            # Add metadata to help VS Code find it
            kernel_config["metadata"] = {
                "interpreter": {
                    "path": venv_python
                }
            }
            
            # Write back the updated kernel.json
            with open(kernel_json_path, 'w') as f:
                json.dump(kernel_config, f, indent=2)
            
            print(f"✅ Updated kernel configuration at: {kernel_json_path}")
            
        except Exception as e:
            print(f"⚠️  Could not update kernel.json: {e}")
    else:
        print(f"⚠️  Kernel directory not found at: {kernel_dir}")
    
    # Verify kernel installation
    verify_kernel_installation(kernel_name, display_name, venv_python)

    # Step 5: Setup NLP resources
    print("\n📚 Step 5: Setting up NLP resources...")
    setup_nltk_data_in_venv(venv_python)
    setup_spacy_models_in_venv(venv_python)
    setup_geoparser_in_venv(venv_python)

    # Step 4: Install VS Code extensions
    print("\n🔧 Step 4: Installing VS Code extensions...")
    vscode_cmd = check_vscode_installed()
    
    if vscode_cmd:
        # Essential extensions from install_extensions.py
        extensions = [
            # Python Development
            ("ms-python.python", "Python"),
            ("ms-python.pylint", "Pylint (Python Linting)"),
            
            # Jupyter Notebooks
            ("ms-toolsai.jupyter", "Jupyter"),
            ("ms-toolsai.jupyter-keymap", "Jupyter Keymap"),
            ("ms-toolsai.jupyter-renderers", "Jupyter Notebook Renderers"),
            
            # Data Science & Visualization
            ("mechatroner.rainbow-csv", "Rainbow CSV"),
            ("GrapeCity.gc-excelviewer", "Excel Viewer"),
            
            # Productivity & UI
            ("ms-vscode.vscode-json", "JSON Language Features"),
            ("redhat.vscode-yaml", "YAML Support"),
            ("yzhang.markdown-all-in-one", "Markdown All in One"),
            ("shd101wyy.markdown-preview-enhanced", "Markdown Preview Enhanced"),
            
            # Code Quality & IntelliSense
            ("ms-vscode.vscode-typescript-next", "TypeScript and JavaScript"),
            ("ms-vscode-remote.vscode-remote-extensionpack", "Remote Development"),
            
            # Additional Helpful Extensions
            ("streetsidesoftware.code-spell-checker", "Code Spell Checker"),
        ]
        
        failed_extensions = []
        for extension_id, extension_name in extensions:
            if not install_vscode_extension(vscode_cmd, extension_id, extension_name):
                failed_extensions.append(extension_name)
    else:
        print("⚠️  VS Code command not found - skipping automatic extension installation")
        print("💡 Since you're clearly using VS Code, you can install these extensions manually:")
        print("\n📦 Essential Extensions to Install:")
        
        essential_extensions = [
            "Python (ms-python.python)",
            "Jupyter (ms-toolsai.jupyter)", 
            "Jupyter Keymap (ms-toolsai.jupyter-keymap)",
            "Jupyter Notebook Renderers (ms-toolsai.jupyter-renderers)",
            "Rainbow CSV (mechatroner.rainbow-csv)",
        ]
        
        for ext in essential_extensions:
            print(f"   • {ext}")
            
        print("\n🔧 How to install extensions manually:")
        print("   1. Press Ctrl+Shift+X in VS Code")
        print("   2. Search for each extension name")
        print("   3. Click 'Install'")
        print("\n✅ Your Python environment will work perfectly without these extensions!")
        print("📚 Extensions just add convenience features like better syntax highlighting")
        
        failed_extensions = []  # Don't count as failures since this is expected

    # Step 5: Create a comprehensive test notebook
    print("\n📝 Step 5: Creating test notebook...")
    
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Digital Studies 101 - Environment Test\n",
                    "\n",
                    "If you can run all the cells below without errors, your setup is working! 🎉\n",
                    "\n",
                    "## Package Imports Test"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test core data science packages\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n", 
                    "import seaborn as sns\n",
                    "import plotly.express as px\n",
                    "import plotly.graph_objects as go\n",
                    "\n",
                    "print(\"✅ Core data science packages imported successfully!\")\n",
                    "print(f\"Pandas version: {pd.__version__}\")\n",
                    "print(f\"NumPy version: {np.__version__}\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test NLP packages\n",
                    "import nltk\n",
                    "import spacy\n",
                    "\n",
                    "print(\"✅ NLP packages imported successfully!\")\n",
                    "print(f\"NLTK version: {nltk.__version__}\")\n",
                    "print(f\"spaCy version: {spacy.__version__}\")\n",
                    "\n",
                    "# Test spaCy model\n",
                    "try:\n",
                    "    nlp = spacy.load('en_core_web_sm')\n",
                    "    doc = nlp('Hello world! This is a test.')\n",
                    "    print(f\"✅ spaCy model working: Found {len(doc)} tokens\")\n",
                    "except OSError:\n",
                    "    print(\"⚠️  spaCy model not found - run: python -m spacy download en_core_web_sm\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test Reddit scraping package\n",
                    "import praw\n",
                    "print(\"✅ PRAW (Reddit API) imported successfully!\")\n",
                    "print(f\"PRAW version: {praw.__version__}\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test machine learning packages\n",
                    "import torch\n",
                    "import transformers\n",
                    "import scipy\n",
                    "import sklearn\n",
                    "\n",
                    "print(\"✅ Machine learning packages imported successfully!\")\n",
                    "print(f\"PyTorch version: {torch.__version__}\")\n",
                    "print(f\"Transformers version: {transformers.__version__}\")\n",
                    "print(f\"SciPy version: {scipy.__version__}\")\n",
                    "print(f\"Scikit-learn version: {sklearn.__version__}\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Create a test visualization\n",
                    "import matplotlib.pyplot as plt\n",
                    "import numpy as np\n",
                    "\n",
                    "# Create sample data\n",
                    "x = np.linspace(0, 10, 100)\n",
                    "y1 = np.sin(x)\n",
                    "y2 = np.cos(x)\n",
                    "\n",
                    "# Create matplotlib plot\n",
                    "plt.figure(figsize=(10, 6))\n",
                    "plt.plot(x, y1, label='sin(x)', linewidth=2)\n",
                    "plt.plot(x, y2, label='cos(x)', linewidth=2)\n",
                    "plt.title('Setup Test - Matplotlib Visualization', fontsize=16)\n",
                    "plt.xlabel('x')\n",
                    "plt.ylabel('y')\n",
                    "plt.legend()\n",
                    "plt.grid(True, alpha=0.3)\n",
                    "plt.show()\n",
                    "\n",
                    "print(\"✅ Matplotlib visualization created successfully!\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Create an interactive Plotly visualization\n",
                    "import plotly.express as px\n",
                    "import pandas as pd\n",
                    "\n",
                    "# Create sample data\n",
                    "df = pd.DataFrame({\n",
                    "    'x': np.linspace(0, 10, 50),\n",
                    "    'y': np.sin(np.linspace(0, 10, 50)),\n",
                    "    'category': ['A'] * 25 + ['B'] * 25\n",
                    "})\n",
                    "\n",
                    "# Create interactive plot\n",
                    "fig = px.scatter(df, x='x', y='y', color='category', \n",
                    "                 title='Setup Test - Interactive Plotly Visualization',\n",
                    "                 hover_data=['x', 'y'])\n",
                    "fig.show()\n",
                    "\n",
                    "print(\"✅ Plotly interactive visualization created successfully!\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🎉 Congratulations!\n",
                    "\n",
                    "If all the cells above ran without errors, your Digital Studies 101 environment is fully set up and ready to go!\n",
                    "\n",
                    "### What you now have:\n",
                    "- ✅ Complete Jupyter environment\n",
                    "- ✅ Data science packages (pandas, numpy, matplotlib, seaborn, plotly)\n",
                    "- ✅ NLP packages (nltk, spacy)\n",
                    "- ✅ Reddit scraping tools (praw)\n",
                    "- ✅ Machine learning tools (torch, transformers, scipy, scikit-learn)\n",
                    "- ✅ VS Code extensions for Python and Jupyter\n",
                    "- ✅ Interactive visualizations\n",
                    "\n",
                    "### Next steps:\n",
                    "1. Always select **\"DS101_env\"** as your kernel in new notebooks\n",
                    "2. Start working on your course assignments!\n",
                    "3. If you have issues, try restarting VS Code or re-running the setup script"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": display_name,
                "language": "python",
                "name": kernel_name
            },
            "language_info": {
                "name": "python",
                "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open("test_setup.ipynb", "w", encoding='utf-8') as f:
        json.dump(notebook_content, f, indent=2)
    
    print("✅ Created comprehensive test_setup.ipynb")

def verify_kernel_installation(kernel_name, display_name, venv_python):
    """Verify that the Jupyter kernel is properly installed and accessible."""
    print("\n🔍 Verifying kernel installation...")
    
    try:
        # Check if kernel is listed in available kernels
        result = subprocess.run(["jupyter", "kernelspec", "list"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and kernel_name in result.stdout:
            print(f"✅ Kernel '{display_name}' found in Jupyter kernel list")
            
            # Try to get kernel info
            result2 = subprocess.run(["jupyter", "kernelspec", "list", "--json"], 
                                   capture_output=True, text=True, timeout=30)
            if result2.returncode == 0:
                try:
                    kernels = json.loads(result2.stdout)
                    if kernel_name in kernels.get('kernelspecs', {}):
                        kernel_info = kernels['kernelspecs'][kernel_name]
                        print(f"✅ Kernel path: {kernel_info['spec']['argv'][0]}")
                        print(f"✅ Display name: {kernel_info['spec']['display_name']}")
                        return True
                except json.JSONDecodeError:
                    pass
        else:
            print(f"❌ Kernel '{kernel_name}' not found in Jupyter kernel list")
            print("Available kernels:")
            if result.returncode == 0:
                print(result.stdout)
            
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"⚠️  Could not verify kernel installation: {e}")
        print("💡 This might be normal if Jupyter is not in the system PATH")
    
    return False

    # Step 6: Create VS Code workspace settings + global configuration
    print("\n⚙️  Step 6: Configuring VS Code...")
    
    # Create local workspace settings with comprehensive configuration
    os.makedirs(".vscode", exist_ok=True)
    
    # Convert to absolute path for consistency
    abs_venv_python = os.path.abspath(venv_python)
    
    vscode_settings = {
        "python.defaultInterpreterPath": abs_venv_python,
        "python.pythonPath": abs_venv_python,
        "jupyter.kernels.filter": [
            {
                "path": abs_venv_python,
                "type": "pythonEnvironment"
            }
        ],
        "jupyter.interactiveWindow.creationMode": "perFile",
        "jupyter.notebookFileRoot": "${workspaceFolder}",
        "notebook.defaultKernel": kernel_name,
        "python.terminal.activateEnvironment": False,
        "python.condaPath": "",
        "python.venvPath": os.path.dirname(venv_path),
        "python.analysis.extraPaths": [venv_path],
        "files.associations": {
            "*.ipynb": "jupyter-notebook"
        }
    }
    
    with open(".vscode/settings.json", "w", encoding='utf-8') as f:
        json.dump(vscode_settings, f, indent=4)
    
    print("✅ Local VS Code settings configured with absolute paths")
    
    # Also try to set global VS Code user settings to prefer the DS101 kernel
    try:
        if platform.system() == "Darwin":  # macOS
            vscode_user_settings_path = os.path.expanduser("~/Library/Application Support/Code/User/settings.json")
        elif platform.system() == "Windows":
            vscode_user_settings_path = os.path.expanduser("~/AppData/Roaming/Code/User/settings.json")
        else:  # Linux
            vscode_user_settings_path = os.path.expanduser("~/.config/Code/User/settings.json")
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(vscode_user_settings_path), exist_ok=True)
        
        # Read existing global settings if they exist
        global_settings = {}
        if os.path.exists(vscode_user_settings_path):
            try:
                with open(vscode_user_settings_path, "r", encoding='utf-8') as f:
                    global_settings = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("⚠️  Could not read existing VS Code settings, creating new ones")
        
        # Add DS101 kernel to global settings (but don't override default interpreter)
        if "jupyter.kernels.filter" not in global_settings:
            global_settings["jupyter.kernels.filter"] = []
        
        # Add our kernel to the filter list if not already there
        ds101_kernel = {
            "path": venv_python,
            "type": "pythonEnvironment"
        }
        
        if ds101_kernel not in global_settings["jupyter.kernels.filter"]:
            global_settings["jupyter.kernels.filter"].append(ds101_kernel)
        
        global_settings["jupyter.interactiveWindow.creationMode"] = "perFile"
        
        # Write updated global settings
        with open(vscode_user_settings_path, "w", encoding='utf-8') as f:
            json.dump(global_settings, f, indent=4)
        
        print("✅ Global VS Code settings updated")
        print("💡 The DS101 kernel is now available in all VS Code projects!")
        
    except Exception as e:
        print(f"⚠️  Could not configure global VS Code settings: {e}")
        print("💡 You'll need to select the kernel manually in new projects")

    # Final summary
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    
    if failed_packages:
        print(f"\n⚠️  Some packages failed to install: {', '.join(failed_packages)}")
        print("💡 You can install these manually later if needed")
    
    if not vscode_cmd:
        print(f"\n✅ VS Code extensions skipped (command line access not available)")
        print("💡 Your Python environment is fully functional!")
        print("💡 Extensions can be installed manually for extra convenience")
    elif 'failed_extensions' in locals() and failed_extensions and vscode_cmd:
        print(f"\n⚠️  Some VS Code extensions failed to install: {len(failed_extensions)}")
        print("💡 You can install these manually through the VS Code Extensions marketplace")
    
    print("\n📋 What to do next:")
    print("1. Close VS Code completely (all windows)")
    print("2. Wait 5-10 seconds")
    print("3. Restart VS Code and open this folder") 
    print("4. Open the file: test_setup.ipynb")
    print("5. When prompted, select kernel: 'Python 3 (DS101)'")
    print("6. If kernel is not visible, try:")
    print("   • Ctrl+Shift+P -> 'Python: Select Interpreter'")
    print(f"   • Choose: {abs_venv_python}")
    print("   • Or use 'Jupyter: Select Kernel' -> 'Python 3 (DS101)'")
    print("7. Run all cells to test your setup")
    
    print("\n🌍 Working with New Projects:")
    print("• Your DS101 kernel is registered globally and available everywhere")
    print("• In any new repo/folder, just select 'Python 3 (DS101)' kernel")
    print("• All packages will be available automatically")
    print("• The virtual environment stays in this setup folder")
    
    print("\n💡 Tips:")
    print("• Always select 'Python 3 (DS101)' as your kernel in notebooks")
    print("• If packages seem missing in new projects, check kernel selection")
    print("• You can re-run this script anytime to update packages")
    print("• The virtual environment is portable - you can copy this whole folder")
    print("\n🛠️  Troubleshooting - If kernel doesn't appear after restart:")
    print("1. Check VS Code Python extension is installed and enabled")
    print("2. Try: Ctrl+Shift+P -> 'Python: Refresh Kernels'")
    print("3. Try: Ctrl+Shift+P -> 'Jupyter: Refresh Kernels'")
    print("4. Manually select interpreter in bottom status bar")
    print("5. If still issues, re-run this setup script")
    print(f"6. Manual kernel path: {abs_venv_python}")
    
    print(f"\n🐍 Virtual Environment Details:")
    print(f"• Location: {venv_path}")
    print(f"• Python executable: {venv_python}")
    print(f"• Kernel registered globally as: {display_name}")
    print("• Packages installed in isolated environment (no conflicts!)")
    print("• Works around Homebrew 'externally-managed-environment' restrictions")
    print("🎯 Complete Digital Studies 101 environment ready!")

if __name__ == "__main__":
    main()