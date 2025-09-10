#!/usr/bin/env python3
"""
Digital Studies 101 - VS Code Extensions Installation Script

This script installs recommended VS Code extensions for the Digital Studies course,
including Python development, Jupyter notebooks, data visualization, and productivity tools.

Requirements:
- Visual Studio Code installed
- Python 3.8 or higher
- Internet connection for downloading extensions

Compatible with:
- Windows 10/11
- macOS 10.15+ 
- Linux (Ubuntu 18.04+)
"""

import subprocess
import sys
import platform
import shutil
import os

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
    
    # Platform-specific checks for Windows
    system = platform.system()
    if system == "Windows":
        print("🔍 Searching for VS Code in common Windows locations...")
        # Check common Windows installation paths
        username = os.getenv('USERNAME', '')
        possible_paths = [
            r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
            r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd".format(username),
            # Also try the direct executable
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe", 
            r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(username),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    # Test if this path works
                    result = subprocess.run([path, "--version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        print(f"✅ Found working VS Code at: {path}")
                        return path
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    continue
    
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
    
    print("❌ Visual Studio Code not found or not working")
    print("💡 Please install VS Code from: https://code.visualstudio.com/")
    print("💡 After installation, you may need to:")
    print("   - Restart your terminal/command prompt")
    print("   - Add VS Code to your PATH")
    print("   - On Windows: Use 'Add to PATH' option during installation")
    return None

def install_extension(vscode_cmd, extension_id, extension_name):
    """Install a single VS Code extension."""
    try:
        print(f"📦 Installing {extension_name}...")
        
        # Try the installation with better error capture
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
    except FileNotFoundError:
        print(f"❌ VS Code command not found when installing {extension_name}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error installing {extension_name}: {e}")
        return False

def main():
    """Main installation function."""
    print("🚀 VS Code Extensions Installation for Digital Studies 101")
    print("=" * 60)
    
    # Check if VS Code is installed
    vscode_cmd = check_vscode_installed()
    if not vscode_cmd:
        sys.exit(1)
    
    # Essential extensions for the course
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
        
        # Git & Version Control
        
        
        # Productivity & UI
        ("ms-vscode.vscode-json", "JSON Language Features"),
        ("redhat.vscode-yaml", "YAML Support"),
        ("yzhang.markdown-all-in-one", "Markdown All in One"),
        ("shd101wyy.markdown-preview-enhanced", "Markdown Preview Enhanced"),
        
        # Code Quality & IntelliSense
        ("ms-vscode.vscode-typescript-next", "TypeScript and JavaScript"),
        ("ms-vscode-remote.vscode-remote-extensionpack", "Remote Development"),
        
        # Theme & Appearance (Optional but nice)
       
        
        # Additional Helpful Extensions
       
        ("streetsidesoftware.code-spell-checker", "Code Spell Checker"),
    ]
    
    print(f"\n📋 Installing {len(extensions)} recommended extensions...")
    print("-" * 60)
    
    failed_extensions = []
    for extension_id, extension_name in extensions:
        if not install_extension(vscode_cmd, extension_id, extension_name):
            failed_extensions.append(extension_name)
    
    print(f"\n🎯 Installation Summary")
    print("=" * 60)
    
    if failed_extensions:
        print(f"❌ Failed to install {len(failed_extensions)} extension(s):")
        for ext in failed_extensions:
            print(f"  • {ext}")
        print("\n💡 You can install these manually through VS Code Extensions marketplace")
    else:
        print("✅ All extensions installed successfully!")
    
    print(f"\n📋 What's included:")
    print("• Python Development: Syntax highlighting, debugging, linting")
    print("• Jupyter Notebooks: Full notebook support with renderers")
    print("• Data Science: CSV viewing, Excel support")
    print("• Git Integration: Enhanced git features and GitHub integration")
    print("• Productivity: Markdown support, spell checking, themes")
    print("• Code Quality: Error highlighting, auto-formatting")
    
    print(f"\n💡 Next Steps:")
    print("1. Restart VS Code to activate all extensions")
    print("2. Open your course folder in VS Code")
    print("3. Select Python interpreter (Ctrl+Shift+P → 'Python: Select Interpreter')")
    print("4. Start working with your Jupyter notebooks!")
    
    print(f"\n🔧 Configuration Tips:")
    print("• Use Ctrl+Shift+P to access the Command Palette")
    print("• Install additional extensions from the Extensions marketplace (Ctrl+Shift+X)")
    print("• Configure Python interpreter for your virtual environment")
    print("• Enable auto-save: File → Auto Save")
    
    print(f"\n🎉 Setup complete! VS Code is ready for Digital Studies 101.")

if __name__ == "__main__":
    main()
