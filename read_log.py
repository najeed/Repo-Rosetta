import os

def read_log_chunks(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, "r", encoding="utf-16le") as f:
        content = f.read()
    
    # Print in chunks of 1000 chars
    chunk_size = 1000
    for i in range(0, len(content), chunk_size):
        print(f"--- CHUNK {i//chunk_size} ---")
        print(content[i:i+chunk_size])

if __name__ == "__main__":
    read_log_chunks("pytest_output.log")
