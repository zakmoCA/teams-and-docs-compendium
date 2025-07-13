from pathlib import Path
from ingest.doc_ingest import extract_text
from summarise.summariser import summarize_text

DOCS_DIR = Path("docs")
PARSED_DIR = Path("parsed_docs")
SUMMARY_DIR = Path("summarise/summaries")

PARSED_DIR.mkdir(exist_ok=True, parents=True)
SUMMARY_DIR.mkdir(exist_ok=True, parents=True)

for doc_path in DOCS_DIR.iterdir():
    try:
        print(f"...processing: {doc_path.name}")
        text = extract_text(doc_path)

        # save parsed text
        parsed_file = PARSED_DIR / (doc_path.stem + ".txt")
        parsed_file.write_text(text)

        # summarise
        summary = summarize_text(text)
        summary_file = SUMMARY_DIR / (doc_path.stem + "_summary.txt")
        summary_file.write_text(summary)

        print(f"✅ {doc_path.name} processed successfully")

    except Exception as e:
        print(f"failed to process {doc_path.name}: {e}")
