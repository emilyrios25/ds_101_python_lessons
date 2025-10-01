# DS 101: Python Data Science Lessons

A comprehensive series of hands-on lessons that teach students how to scrape, wrangle, analyze, and visualize data from Reddit using Python. This package provides a complete data science workflow from data collection to advanced analysis techniques including geospatial analysis and sentiment analysis.

## 🎯 Learning Objectives

By completing these lessons, students will learn to:
- Scrape data from social media platforms (Reddit) using APIs
- Clean and wrangle messy real-world data using pandas
- Extract geographic information from text using NLP techniques
- Perform sentiment analysis using both rule-based (VADER) and transformer-based (RoBERTa) models
- Create interactive visualizations and maps using plotly
- Handle large datasets and machine learning model deployment challenges

## 📚 Lesson Overview

### Lesson 1: Reddit Data Scraping
**File:** `lesson_1_scraping_reddit/lesson_1_scraping_reddit.ipynb`
- Set up Reddit API credentials (PRAW library)
- Learn web scraping ethics and rate limiting
- Collect posts and comments from specific subreddits
- Handle API authentication and data export
- **Output:** Raw Reddit data in CSV and pickle formats

### Lesson 2: Basic Python & Data Structures
**File:** `lesson_2_very_basic_python/lesson_2_very_basic_python.ipynb`
- Python fundamentals for data science
- Working with lists, dictionaries, and data structures
- Introduction to pandas DataFrames
- Basic data manipulation techniques

### Lesson 3: Data Wrangling with Pandas
**File:** `lesson_3_introduction_pandas/lesson 3_introduction_pandas_datawrangling.ipynb`
- Advanced pandas operations for data cleaning
- Handling missing data and duplicates
- Data transformation and aggregation
- Preparing data for analysis
- **Input:** Raw Reddit data from Lesson 1

### Lesson 4: Geospatial Analysis & Location Extraction
**Files:** 
- `lesson_4_finding_locations/lesson_4_1_extracting_locations.ipynb` - Basic toponym extraction using NER
- `lesson_4_finding_locations/lesson_4_2_geoparsing_mapping.ipynb` - Advanced geoparsing and mapping
- `lesson_4_finding_locations/lesson_4_3_model_training.ipynb` - Custom geoparser model training

**Lesson 4.1:** Extract place names (toponyms) from text using Natural Language Processing and known place name matching
**Lesson 4.2:** Use sophisticated geoparsing library to resolve geographic references and create interactive maps  
**Lesson 4.3:** Train custom geoparser models for domain-specific text and improved accuracy
- **Output:** Geoparsed data with coordinates and trained custom models

### Lesson 5: Sentiment Analysis
**File:** `lesson_5_sentiment_analysis/lesson_5_sentiment_analysis.ipynb`
- Compare rule-based (NLTK VADER) vs transformer-based (RoBERTa) sentiment analysis
- Analyze sentiment of location-containing text
- Visualize sentiment patterns across geographic regions
- Evaluate model performance and limitations
- Create correlation analyses between sentiment and engagement metrics

## 🚀 Quick Start with Automated Setup

This repository includes an automated setup system that creates a complete Python virtual environment with all required dependencies.

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux
- Internet connection (for downloading packages and ML models)

### One-Command Setup
```bash
python manual_setup.py
```

### What `manual_setup.py` Does
The automated setup script provides a **bulletproof installation process** that:

1. **Creates Isolated Environment**: Builds a dedicated virtual environment (`ds101_manual`) to prevent package conflicts
2. **Installs All Dependencies**: Automatically installs 20+ required packages including:
   - Data manipulation: `pandas`, `numpy`
   - Web scraping: `praw` (Reddit API)
   - NLP & Sentiment: `nltk`, `transformers`, `torch`, `spacy`
   - Geospatial: `geopandas`, `geopy`
   - Visualization: `plotly`, `matplotlib`
   - Jupyter ecosystem: `jupyter`, `ipykernel`

3. **Pre-downloads ML Models**: Downloads and caches large models (like RoBERTa ~500MB) to prevent classroom delays
4. **Configures Jupyter Integration**: Registers the environment as a Jupyter kernel for seamless notebook execution
5. **Validates Installation**: Runs comprehensive tests to ensure everything works correctly

### Why This Setup Prevents Hiccups

**🛡️ Isolation**: Virtual environment prevents conflicts with existing Python installations
**📦 Version Control**: Locks specific package versions that are known to work together
**🤖 Model Pre-caching**: Downloads transformer models ahead of time (prevents 15+ minute delays during class)
**🧪 Validation**: Tests all components before students start lessons
**🔄 Reproducibility**: Ensures identical environments across all student machines


## 🔧 Technical Requirements

### Minimum System Requirements
- **RAM**: 4GB (8GB recommended for transformer models)
- **Storage**: 2GB free space (includes ML models)
- **Python**: 3.8-3.11 (3.12+ may have package compatibility issues)

### Key Dependencies
- **Core**: pandas, numpy, jupyter
- **API Access**: praw (Reddit), requests
- **NLP**: nltk, spacy, transformers, torch
- **Geospatial**: geopandas, geopy, folium
- **Visualization**: plotly, matplotlib, seaborn
- **ML**: scikit-learn, scipy


## 📜 License

This educational content is designed for academic use. Please respect Reddit's API terms of service and rate limiting guidelines when using these materials.

---

**Note for Students**: Always run `python manual_setup.py` first to ensure your environment is properly configured before starting the lessons!
