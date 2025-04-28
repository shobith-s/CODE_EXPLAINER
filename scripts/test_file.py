import os

data_dir = "../data"
os.makedirs(data_dir, exist_ok=True)
test_file = os.path.join(data_dir, "test.txt")
with open(test_file, "w", encoding="utf-8") as f:
    f.write("Test successful!")
print(f"Test file created at: {os.path.abspath(test_file)}")
from transformers import pipeline
print("Pipeline imported successfully!")