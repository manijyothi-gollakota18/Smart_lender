import os
import urllib.request

def download_dataset():
    url = "https://raw.githubusercontent.com/sahutkarsh/loan-prediction-analytics-vidhya/master/train.csv"
    dest_dir = "data"
    dest_file = os.path.join(dest_dir, "train.csv")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")
        
    print(f"Downloading dataset from {url}...")
    try:
        urllib.request.urlretrieve(url, dest_file)
        print(f"Dataset successfully downloaded and saved to: {dest_file}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    download_dataset()
