# Reddit Comment Scraper - Lesson 1

A comprehensive Python-based tool for scraping Reddit comments and posts for text analysis and digital studies research.

## 📋 Overview

This lesson teaches students how to:
- Extract comments from individual Reddit threads
- Scrape entire subreddits for large-scale text analysis
- Save data in formats suitable for analysis tools like Voyant
- Use authenticated Reddit API access for higher rate limits

## 🚀 Quick Start

1. **Install Dependencies** (see below)
2. **Open** `lesson_1_scraping_reddit.ipynb` in VS Code or Jupyter
3. **Run cells sequentially** starting from the top
4. **Modify settings** as needed (URLs, subreddit names, etc.)
5. **Find your data** in the `data/` folder

## 📦 Required Dependencies

### Core Python Packages
Install these packages using pip:

```bash
pip install praw pandas cryptography
```

### Detailed Package Requirements

#### 1. **PRAW (Python Reddit API Wrapper)**
```bash
pip install praw
```
- **Purpose**: Interface with Reddit's API
- **Version**: Latest stable (7.0+)
- **Used for**: Authentication, data retrieval, rate limiting

#### 2. **Pandas**
```bash
pip install pandas
```
- **Purpose**: Data manipulation and CSV export
- **Version**: Latest stable (1.5+)
- **Used for**: DataFrame creation, data cleaning, file export

#### 3. **Cryptography**
```bash
pip install cryptography
```
- **Purpose**: Decrypt instructor's Reddit credentials
- **Version**: Latest stable (40.0+)
- **Used for**: Fernet encryption/decryption for secure authentication

### Built-in Python Libraries
These are included with Python (no installation needed):
- `datetime` - Timestamp formatting
- `os` - File and directory operations
- `sys` - System operations for module reloading
- `importlib` - Dynamic module imports
- `base64` - Fallback encoding for credentials

## 📁 File Structure

```
lesson_1_scraping_reddit/
├── README.md                          # This file
├── lesson_1_scraping_reddit.ipynb     # Main lesson notebook
├── reddit_auth.py                     # Authentication module
├── reddit_config_encrypted.py         # Encrypted credentials
├── data/                              # Output folder (created automatically)
│   ├── reddit_text_analysis_*.csv     # Structured data
│   └── reddit_voyant_*.txt            # Text-only files for Voyant
└── .gitignore                         # Git ignore file
```

## 🔧 Authentication System

### For Students (No Setup Required)
- **Encrypted credentials** are provided automatically
- **Higher rate limits** (600 requests/minute vs 60)
- **No Reddit account** needed
- **Secure** - credentials cannot be reverse-engineered

### For Instructors (Setup Required)
To set up your own encrypted credentials:

1. **Create Reddit App**:
   - Go to https://www.reddit.com/prefs/apps
   - Create "script" application
   - Note client_id and client_secret

2. **Run encryption script**:
   ```python
   python encrypt_credentials.py
   ```

3. **Update config file** with your encrypted credentials

## 📊 Rate Limits & Authentication

| Authentication Method | Rate Limit | Best For |
|----------------------|------------|----------|
| **Authenticated (Encrypted)** | 600 requests/minute | Large subreddits, many posts |
| **Anonymous (Read-only)** | 60 requests/minute | Single threads, small datasets |

## 💾 Output Files

### CSV Files (`data/reddit_text_analysis_*.csv`)
Structured data with columns:
- `type`: "post" or "comment"
- `title`: Thread title (for context)
- `text`: The actual text content
- `date`: When it was posted
- `score`: Reddit score (upvotes - downvotes)

### TXT Files (`data/reddit_voyant_*.txt`)
Plain text files perfect for:
- **Voyant Tools** (voyant-tools.org)
- **Word cloud generators**
- **Text analysis software**

## 🎯 Usage Examples

### Basic Thread Scraping
```python
# Change the URL to any Reddit thread
url = "https://www.reddit.com/r/AskReddit/comments/..."
```

### Subreddit Scraping
```python
subreddit_name = "JMU"        # Any subreddit
num_posts = 100               # Number of posts to scrape
sort_method = "top"           # "hot", "new", "top", "rising"
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'praw'
   ```
   **Solution**: Install required packages
   ```bash
   pip install praw pandas cryptography
   ```

2. **Authentication Failures**
   ```
   ❌ Setup failed: Connection error
   ```
   **Solution**: Check internet connection, restart kernel

3. **No Data Collected**
   ```
   ❌ No text data to save
   ```
   **Solution**: Check subreddit name spelling, try different sort method

### Getting Help

1. **Restart Jupyter Kernel**: Kernel → Restart
2. **Clear All Outputs**: Cell → All Output → Clear
3. **Run cells in order** from top to bottom
4. **Check internet connection**
5. **Verify subreddit exists** and is public

## 📚 Educational Use

This tool is designed for:
- **Digital Studies courses**
- **Text analysis research**
- **Social media studies**
- **Data science education**

### Learning Objectives
- Understand API authentication
- Practice data extraction techniques
- Learn text preprocessing
- Explore social media data patterns

## 🔒 Privacy & Ethics

- **Respect Reddit's Terms of Service**
- **Use for educational purposes only**
- **Don't collect personal information**
- **Be mindful of rate limits**
- **Consider user privacy** in research

## 📈 Data Analysis Next Steps

After collecting data, students can:
1. **Upload TXT files to Voyant Tools**
2. **Analyze CSV files in Excel/Google Sheets**
3. **Create word clouds**
4. **Perform sentiment analysis**
5. **Study temporal patterns**

## 🤝 Contributing

For instructors wanting to modify or extend this lesson:
1. Fork the repository
2. Create feature branch
3. Test thoroughly with students
4. Submit pull request

## 📄 License

This educational material is provided for academic use. Please credit the original authors when using or adapting this content.

---

**Created for Digital Studies at James Madison University**  
**Instructor**: [Your Name]  
**Course**: [Course Code/Name]  
**Semester**: [Current Semester]
