import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from ingest.doc_ingest import extract_text
from summarise.summariser import summarize_text

DOCS_DIR = Path("docs")
PARSED_DIR = Path("parsed_docs")
SUMMARY_DIR = Path("summarise/summaries")

PARSED_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

for doc_path in DOCS_DIR.iterdir():
    if not doc_path.is_file():
        continue

    try:
        print(f"...processing: {doc_path.name}")
        text = extract_text(doc_path)

        parsed_file = PARSED_DIR / f"{doc_path.stem}.txt"
        parsed_file.write_text(text, encoding="utf-8")

        # generate markdown summary
        summary_raw = summarize_text(text).strip()
        if summary_raw.startswith("```markdown") and summary_raw.endswith("```"):
            summary_clean = "\n".join(summary_raw.splitlines()[1:-1]).strip()
        else:
            summary_clean = summary_raw

        summary_file = SUMMARY_DIR / f"{doc_path.stem}_summary.md"
        summary_file.write_text(summary_clean, encoding="utf-8")

        print(f"✅ {doc_path.name} processed successfully")

    except Exception as e:
        print(f"❌ failed to process {doc_path.name}: {e}")
