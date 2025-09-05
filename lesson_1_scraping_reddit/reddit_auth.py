# Reddit Authentication Helper
# This module handles all the complex authentication for students

import praw
import os

def setup_reddit_connection():
    """
    Set up Reddit connection with the best available authentication method.
    
    Returns:
        tuple: (reddit_instance, auth_mode, rate_limit)
        - reddit_instance: Configured PRAW Reddit object
        - auth_mode: "authenticated" or "read-only" 
        - rate_limit: Number of requests per minute
    """
    
    def decrypt_credential(encrypted_data, key):
        """Decrypt credentials using Fernet encryption"""
        try:
            from cryptography.fernet import Fernet
            f = Fernet(key)
            return f.decrypt(encrypted_data.encode()).decode()
        except ImportError:
            # Silently try fallback method
            import base64
            try:
                return base64.b64decode(encrypted_data).decode()
            except:
                return None
        except Exception:
            # Silent failure - let calling code handle messaging
            return None

    # Initialize default variables
    reddit_username = None
    reddit_password = None
    client_id = "BQ9nZDrIpdsq_2d67qopWw"
    client_secret = "EE8yF4d_F6i-Kc30HPWtaRRobELhSQ"
    user_agent = "educational-scraper/1.0 (for academic research)"

    # Method 1: Try environment variables first (most secure)
    reddit_username = os.getenv('REDDIT_USERNAME')
    reddit_password = os.getenv('REDDIT_PASSWORD')

    # Method 2: Try encrypted config file
    if not reddit_username or not reddit_password:
        try:
            from lesson_1_scraping_reddit.reddit_config_encrypted import (
                ENCRYPTED_USERNAME, ENCRYPTED_PASSWORD, ENCRYPTION_KEY,
                REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, USER_AGENT
            )
            
            # Use config values
            client_id = REDDIT_CLIENT_ID
            client_secret = REDDIT_CLIENT_SECRET
            user_agent = USER_AGENT
            
            # Decrypt credentials
            reddit_username = decrypt_credential(ENCRYPTED_USERNAME, ENCRYPTION_KEY)
            reddit_password = decrypt_credential(ENCRYPTED_PASSWORD, ENCRYPTION_KEY)
            
            if not reddit_username or not reddit_password:
                # Failed to decrypt, fall back to read-only
                reddit_username = None
                reddit_password = None
                
        except ImportError:
            # No encrypted config available, will use read-only mode
            pass
        except Exception:
            # Error loading config, will use read-only mode
            pass

    # Create Reddit connection
    try:
        if reddit_username and reddit_password:
            # Create authenticated Reddit instance
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=reddit_username,
                password=reddit_password,
                user_agent=user_agent
            )
            
            # Test authentication
            try:
                user = reddit.user.me()
                auth_mode = "authenticated"
                rate_limit = 600
            except Exception:
                # Authentication failed, fall back to read-only
                reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                auth_mode = "read-only"
                rate_limit = 60
            
        else:
            # Create read-only Reddit instance
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            auth_mode = "read-only"
            rate_limit = 60
        
        # Test the connection by accessing a public subreddit
        test_subreddit = reddit.subreddit("python")
        test_post = next(test_subreddit.hot(limit=1))
        
        return reddit, auth_mode, rate_limit
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Possible solutions:")
        print("   • Check internet connection")
        print("   • Verify Reddit API credentials")
        print("   • Try running the cell again")
        print("   • Install required packages: pip install praw cryptography")
        raise e
