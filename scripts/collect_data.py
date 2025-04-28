# Imports at the top
import requests
from bs4 import BeautifulSoup
import json
import os

# Ensure data directory exists relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
data_dir = os.path.join(script_dir, "..", "data")  # Go up one level to code_explainer/data
os.makedirs(data_dir, exist_ok=True)
print(f"Data directory: {os.path.abspath(data_dir)}")

# Fetch Stack Overflow data
def fetch_stackoverflow():
    print("Fetching Stack Overflow data...")
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "site": "stackoverflow",
        "tagged": "python",
        "filter": "!9Z(-wwYGT",  # Ensures title and body
        "pagesize": 10
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        questions = response.json()["items"]
        file_path = os.path.join(data_dir, "stackoverflow.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(questions, f)
        print(f"Stack Overflow data saved to: {file_path}")
    except Exception as e:
        print(f"Error fetching Stack Overflow: {e}")

def fetch_github():
    print("Fetching GitHub data...")
    url = "https://api.github.com/repos/python/cpython/issues"
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    headers = {"Authorization": f"token {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        issues = [issue for issue in response.json() if issue.get("body") is not None]  # Filter out None bodies
        file_path = os.path.join(data_dir, "github.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(issues, f)
        print(f"GitHub data saved to: {file_path}")
    except Exception as e:
        print(f"Error fetching GitHub: {e}")

# Fetch Python documentation
def fetch_python_docs():
    print("Fetching Python docs...")
    url = "https://docs.python.org/3/library/functions.html"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        file_path = os.path.join(data_dir, "python_docs.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Python docs saved to: {file_path}")
    except Exception as e:
        print(f"Error fetching Python docs: {e}")

if __name__ == "__main__":
    fetch_stackoverflow()
    fetch_github()
    fetch_python_docs()
    print("Data collection complete.")