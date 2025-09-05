
#!/usr/bin/env python3
"""
Digital Studies 101 - Python Lessons
Complete Package Installation Script

This script installs all required packages and dependencies for the entire course,
including Reddit scraping, NLP, geoparsing, sentiment analysis, and data visualization.

Requirements:
- Python 3.8 or higher (recommended: Python 3.9+)
- pip package manager
- Internet connection for downloading packages and models

Compatible with:
- Windows 10/11
- macOS 10.15+ 
- Linux (Ubuntu 18.04+)
"""

import subprocess
import sys
import importlib.util
import warnings
warnings.filterwarnings('ignore')

def check_python_version():
    """Check if Python version is compatible."""
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    print(f"🐍 Python version: {sys.version}")
    
    if current_version < min_version:
        print(f"❌ Python {min_version[0]}.{min_version[1]}+ is required, but you have {current_version[0]}.{current_version[1]}")
        print("💡 Please upgrade Python: https://www.python.org/downloads/")
        return False
    else:
        print(f"✅ Python version {current_version[0]}.{current_version[1]} is compatible")
        return True

def check_and_install_package(package_name, import_name=None):
    """Check if a package is installed, install if not."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} already installed")
        return True
    except ImportError:
        print(f"📦 Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name}")
            return False

def check_and_download_nltk_data():
    """Download required NLTK data packages."""
    try:
        import nltk
        
        # Check for required NLTK data
        nltk_data_packages = [
            ('punkt', 'tokenizers/punkt'),         # For sentence tokenization (Lesson 4)
            ('vader_lexicon', 'vader_lexicon'),    # For sentiment analysis (Lesson 5)
        ]
        
        for package, path in nltk_data_packages:
            try:
                nltk.data.find(path)
                print(f"✅ NLTK {package} already available")
            except LookupError:
                print(f"📥 Downloading NLTK {package}...")
                nltk.download(package, quiet=True)
                print(f"✅ NLTK {package} downloaded successfully")
                
    except ImportError:
        print("❌ NLTK not installed - skipping NLTK data downloads")

def check_and_download_spacy_model():
    """Download required spaCy language models."""
    models = ["en_core_web_md", "en_core_web_trf"]
    try:
        import spacy
        for model_name in models:
            try:
                spacy.load(model_name)
                print(f"✅ spaCy model {model_name} already available")
            except OSError:
                print(f"📥 Downloading spaCy model {model_name}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
                    print(f"✅ spaCy model {model_name} downloaded successfully")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to download spaCy model {model_name}")
    except ImportError:
        print("❌ spaCy not installed - skipping model download")

def check_and_setup_geoparser():
    """Setup geoparser and download GeoNames database."""
    try:
        import geoparser
        # Test if geonames data is available by trying to create a Geoparser instance
        try:
            gp = geoparser.Geoparser()
            print("✅ Geoparser and GeoNames data already available")
        except Exception as e:
            print("📥 Downloading GeoNames database (this may take a while)...")
            try:
                subprocess.check_call([sys.executable, "-m", "geoparser", "download", "geonames"])
                print("✅ GeoNames database downloaded successfully")
            except subprocess.CalledProcessError:
                print("❌ Failed to download GeoNames database")
                print("💡 You may need to run this manually: python -m geoparser download geonames")
    except ImportError:
        print("❌ Geoparser not installed - skipping GeoNames database setup")

def main():
    """Main installation function."""
    print("🚀 Starting Digital Studies 101 - Python Lessons Package Installation")
    print("=" * 70)
    
    # Check Python version compatibility
    if not check_python_version():
        print("\n❌ Installation aborted due to incompatible Python version.")
        sys.exit(1)
    
    # Core packages for all lessons
    core_packages = [
        # Basic data science stack
        'pandas',
        'matplotlib',
        
        
        # Interactive visualization
        'plotly',
        'mapclassify',
        
        # Progress bars
        'tqdm',
        
        # Reddit scraping (Lesson 1)
        'praw',
        
        # NLP packages (Lessons 4-5)
        'nltk',
        'spacy',
        'geoparser',
        
        # Machine Learning / Transformers (Lesson 5)
        'transformers',
        'torch',
        'scipy',

        # Utilities
        'cryptography'
               
    ]   
    print("\n📦 Installing core packages...")
    print("-" * 40)
    
    failed_packages = []
    for package in core_packages:
        if not check_and_install_package(package):
            failed_packages.append(package)
    
    print("\n📚 Setting up NLP resources...")
    print("-" * 40)
    
    # Setup NLTK data
    check_and_download_nltk_data()
    
    # Setup spaCy model
    check_and_download_spacy_model()
    
    # Setup geoparser and GeoNames database
    check_and_setup_geoparser()
    
    print("\n🎯 Installation Summary")
    print("=" * 70)
    
    if failed_packages:
        print(f"❌ Failed to install: {', '.join(failed_packages)}")
        print("💡 Try installing these manually with: pip install <package_name>")
    else:
        print("✅ All packages installed successfully!")
    
    print("\n📋 What's included:")
    print("• Lesson 1: Reddit scraping (praw, pandas)")
    print("• Lesson 2: Basic Python (pandas, matplotlib)")
    print("• Lesson 3: Data wrangling (pandas, seaborn, plotly)")
    print("• Lesson 4: Location extraction (spacy, geoparser, nltk)")
    print("• Lesson 5: Sentiment analysis (transformers, torch, scipy)")
    print("• All lessons: Interactive visualization (plotly, mapclassify)")
    
    print("\n💡 Notes:")
    print("• NLTK data packages are automatically downloaded")
    print("• spaCy models (en_core_web_md & en_core_web_trf) are downloaded")
    print("• GeoNames database is downloaded for geoparser")
    print("• All packages support both Windows and macOS")
    
    print("\n🎉 Setup complete! You're ready to start the lessons.")

if __name__ == "__main__":
    main()

