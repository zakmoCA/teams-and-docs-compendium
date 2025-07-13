from pathlib import Path

DOCS_DIR = Path("docs")
PARSED_DIR = Path("parsed_docs")
SUMMARY_DIR = Path("summarise/summaries")

deleted = 0

for doc_path in DOCS_DIR.iterdir():
    if not doc_path.is_file():
        continue

    stem = doc_path.stem
    parsed_file = PARSED_DIR / f"{stem}.txt"
    summary_file = SUMMARY_DIR / f"{stem}_summary.txt"

    for file in [parsed_file, summary_file]:
        if file.exists():
            file.unlink()
            print(f"...deleted {file} ✅")
            deleted += 1

print(f"\n...cleanup complete. {deleted} files removed 🗑️")
