from pathlib import Path

RAW_DATA_DIR = Path("data/raw")

def list_raw_files():
    files = list(RAW_DATA_DIR.glob("*.csv"))

    print("Arquivos encontrados em data/raw:")

    for file in files:
        print(f"- {file}")

if __name__ == "__main__":
    list_raw_files()
