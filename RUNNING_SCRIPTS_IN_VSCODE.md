# Running Installation Scripts in Visual Studio Code

This guide explains how to set up and run the Digital Studies 101 installation scripts directly from Visual Studio Code.

## Prerequisites

1. **Visual Studio Code** installed on your system
2. **Python 3.8+** installed on your system
3. **Git** installed on your system (for cloning the repository)
4. **Internet connection** for downloading packages and extensions

## Step 0: Download the Setup Files

### Option A: Using Git (Recommended)

1. **Open VS Code**
2. **Open the integrated terminal:**
   - Press `` Ctrl+` `` (backtick) OR
   - Go to `View` → `Terminal`

3. **Navigate to where you want to store the setup files:**
   ```bash
   cd repos    # or wherever you prefer
   ```

4. **Clone the setup repository:**
   ```bash
   git clone https://github.com/joostburgers/python_setup_ds_101.git
   ```

5. **Navigate into the cloned folder:**
   ```bash
   cd python_setup_ds_101
   ```


## Step 1: Open the Setup Project in VS Code

1. **If you used Git clone, VS Code should already be in the right directory**

2. **Verify you're in the right place:**
   - You should see files like `installs_required.py` and `install_vscode_extensions.py` in the file explorer

## Method 1: Using VS Code's Integrated Terminal (Recommended)

### Step 2: Open the Integrated Terminal

1. **Open terminal in VS Code:**
   - Press `` Ctrl+` `` (backtick) OR
   - Go to `View` → `Terminal` OR
   - Press `Ctrl+Shift+P` and type "Terminal: Create New Terminal"

2. **Verify you're in the right directory:**
   - The terminal should show the path to your `python_setup_ds_101` folder
   - You should see files like `installs_required.py` and `install_vscode_extensions.py`

### Step 3: Run the Installation Scripts

#### First: Install Python Packages and Dependencies
```bash
python installs_required.py
```
*This installs all the Python packages needed for the course (pandas, matplotlib, spacy, etc.)*

#### Second: Install VS Code Extensions  
```bash
python install_vscode_extensions.py
```
*This installs helpful VS Code extensions for Python development and Jupyter notebooks*

### Step 4: Monitor Progress

- Watch the terminal output for installation progress
- Green checkmarks ✅ indicate successful installations
- Red X marks ❌ indicate failures that may need manual attention
- **The first script may take 15-30 minutes** depending on your internet connection
- **The second script is usually much faster** (2-5 minutes)

## Troubleshooting

### Git Not Found (For Step 0)
**Error:** `'git' is not recognized as an internal or external command`

**Solutions:**
1. **Download Git:** https://git-scm.com/downloads
2. **Use the ZIP download option instead** (Option B in Step 0)
3. **Restart VS Code** after installing Git

### Python Not Found
**Error:** `'python' is not recognized as an internal or external command`

**Solutions:**
1. **Try `python3` instead of `python`:**
   ```bash
   python3 installs_required.py
   ```

2. **Use full Python path:**
   ```bash
   C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python313\python.exe installs_required.py
   ```

3. **Fix Python PATH:**
   - Reinstall Python with "Add to PATH" option checked
   - Or manually add Python to your system PATH

### VS Code Extensions Script Fails
**Error:** VS Code command not found

**Solutions:**
1. **Reinstall VS Code** with "Add to PATH" option
2. **Restart VS Code** after installation
3. **Run as Administrator** if on Windows

### Permission Errors
**Error:** Permission denied or access errors

**Solutions:**
1. **Run VS Code as Administrator** (Windows)
2. **Check file permissions** in terminal:
   ```bash
   ls -la *.py  # On macOS/Linux
   dir *.py     # On Windows
   ```

### Network/Download Issues
**Error:** Timeout or connection errors

**Solutions:**
1. **Check internet connection**
2. **Try running scripts one at a time**
3. **Use a VPN** if behind restrictive firewall
4. **Run during off-peak hours** for large downloads

## Post-Installation

### Verify Python Packages
```bash
python -c "import pandas, matplotlib, plotly, nltk, spacy; print('All packages imported successfully!')"
```

### Verify VS Code Extensions
1. **Open Extensions panel:** `Ctrl+Shift+X`
2. **Check installed extensions:** Look for Python, Jupyter, etc.

### Test Jupyter Notebooks
1. **Open a `.ipynb` file** in VS Code
2. **Select Python kernel** when prompted
3. **Run a test cell** to verify everything works

## Tips for Students

1. **Always use the integrated terminal** - keeps everything in one place
2. **Read the output carefully** - it shows exactly what's happening
3. **Don't panic if something fails** - most issues can be fixed by re-running
4. **Ask for help early** - don't struggle alone with installation issues
5. **Keep VS Code updated** - newer versions have better Python support

## Getting Started Summary

**For students new to this process, here's the quick version:**

1. **Get the setup files:**
   - Go to: https://github.com/joostburgers/python_setup_ds_101
   - Download ZIP or clone with Git

2. **Open in VS Code:**
   - Open the downloaded/cloned folder in VS Code

3. **Run the scripts:**
   - Open terminal in VS Code (`` Ctrl+` ``)
   - Run: `python installs_required.py`
   - Wait for completion, then run: `python install_vscode_extensions.py`

4. **Restart VS Code** when done

## Next Steps

After successful installation:

1. **Restart VS Code** to activate all extensions
2. **Clone or download your course materials** (separate from the setup repository)
3. **Open a Jupyter notebook** to test the environment
4. **Configure Git** if you haven't already:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```
5. **Start working** on your Digital Studies assignments!

---

**Need Help?** 
- **Setup Repository:** https://github.com/joostburgers/python_setup_ds_101
- VS Code Python tutorial: https://code.visualstudio.com/docs/python/python-tutorial
- Python extension documentation: https://marketplace.visualstudio.com/items?itemName=ms-python.python
- Course discussion forum or office hours
