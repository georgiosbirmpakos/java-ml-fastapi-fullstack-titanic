"""
Script to download Titanic dataset from Kaggle
"""

import os
import zipfile
import requests
from pathlib import Path

def download_titanic_data():
    """Download Titanic dataset from Kaggle"""
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Check if data already exists
    train_file = data_dir / "train.csv"
    test_file = data_dir / "test.csv"
    
    if train_file.exists() and test_file.exists():
        print("Titanic dataset already exists!")
        return
    
    print("Downloading Titanic dataset...")
    
    # For this example, we'll provide direct download links
    # In practice, you would use the Kaggle API with authentication
    
    # Alternative: Download from a reliable source
    train_url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    
    try:
        # Download the dataset
        print("Downloading train.csv...")
        response = requests.get(train_url)
        response.raise_for_status()
        
        # Save the data
        with open(train_file, 'wb') as f:
            f.write(response.content)
        
        print(f"Dataset downloaded successfully to {train_file}")
        
        # For the test set, we'll create a sample from the training data
        # In a real scenario, you'd download the actual test set from Kaggle
        print("Creating sample test set...")
        import pandas as pd
        
        # Read the downloaded data
        df = pd.read_csv(train_file)
        
        # Split into train and test (80/20 split)
        from sklearn.model_selection import train_test_split
        
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['Survived'])
        
        # Save train and test sets
        train_df.to_csv(train_file, index=False)
        test_df.to_csv(test_file, index=False)
        
        print(f"Train set saved: {train_file} ({len(train_df)} samples)")
        print(f"Test set saved: {test_file} ({len(test_df)} samples)")
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Please manually download the Titanic dataset from Kaggle:")
        print("https://www.kaggle.com/c/titanic/data")
        print("Place train.csv and test.csv in the data/ directory")

def setup_kaggle_api():
    """Setup instructions for Kaggle API"""
    print("\n" + "="*50)
    print("KAGGLE API SETUP INSTRUCTIONS")
    print("="*50)
    print("1. Go to https://www.kaggle.com/account")
    print("2. Scroll down to 'API' section")
    print("3. Click 'Create New API Token'")
    print("4. Download the kaggle.json file")
    print("5. Place it in your home directory:")
    print("   - Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json")
    print("   - Linux/Mac: ~/.kaggle/kaggle.json")
    print("6. Set permissions: chmod 600 ~/.kaggle/kaggle.json")
    print("\nThen run: python download_data.py --use-kaggle-api")
    print("="*50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--use-kaggle-api":
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            
            # Initialize Kaggle API
            api = KaggleApi()
            api.authenticate()
            
            # Download Titanic dataset
            api.competition_download_files('titanic', path='data', unzip=True)
            print("Titanic dataset downloaded successfully using Kaggle API!")
            
        except Exception as e:
            print(f"Error using Kaggle API: {e}")
            print("Falling back to alternative download method...")
            download_titanic_data()
    else:
        download_titanic_data()
        setup_kaggle_api()
