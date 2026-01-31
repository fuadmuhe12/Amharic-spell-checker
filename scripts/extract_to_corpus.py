"""
Extract Amharic text from JSON files in data/unprocessed_data/ and append to corpus.
Only Amharic letters, space, ። and ፤. Never replaces corpus. Tracks processed files.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNPROCESSED = ROOT / "data" / "unprocessed_data"
CORPUS = ROOT / "data" / "amharic_corpus.txt"
PROCESSED_LOG = ROOT / "data" / "processed_files.txt"

PUNCT = "።፤"
OK_RANGES = [
    (0x1200, 0x1368),
    (0x137D, 0x137F),
    (0x2D80, 0x2DDF),
]


def _allowed(c: str) -> bool:
    if c.isspace() or c in PUNCT:
        return True
    code = ord(c)
    return any(lo <= code <= hi for lo, hi in OK_RANGES)


def clean(text: str) -> str:
    out = []
    for c in text:
        if _allowed(c):
            out.append(c)
        else:
            if out and not out[-1].isspace():
                out.append(" ")
    return " ".join("".join(out).split())


def to_sentences(text: str) -> list[str]:
    parts = re.split(r"[።፤]+", text)
    sents = []
    for p in parts:
        s = p.strip()
        if len(s) > 2:
            if not s.endswith(("።", "፤")):
                s += "።"
            sents.append(s)
    return sents


def get_texts(data) -> list[str]:
    texts = []
    if isinstance(data, list):
        for obj in data:
            if isinstance(obj, dict) and "text" in obj and obj["text"]:
                texts.append(str(obj["text"]).strip())
    elif isinstance(data, dict) and "messages" in data:
        for msg in data["messages"]:
            if isinstance(msg, dict) and "text" in msg and msg["text"]:
                texts.append(str(msg["text"]).strip())
    return texts


def main() -> None:
    sys.path.insert(0, str(ROOT / "src"))

    processed = set()
    if PROCESSED_LOG.exists():
        with open(PROCESSED_LOG, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    processed.add(name)

    if not UNPROCESSED.exists():
        print("No unprocessed_data folder.")
        return

    jsons = sorted(UNPROCESSED.glob("*.json"))
    to_process = [f for f in jsons if f.name not in processed]
    if not to_process:
        print("No new JSON files to process.")
        return

    new_sents = []
    newly_processed = []

    for jpath in to_process:
        try:
            with open(jpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Skip {jpath.name}: {e}")
            continue

        for raw in get_texts(data):
            c = clean(raw)
            if c:
                new_sents.extend(to_sentences(c))
        newly_processed.append(jpath.name)

    if new_sents:
        with open(CORPUS, "a", encoding="utf-8") as f:
            for s in new_sents:
                f.write(s + "\n")
        print(f"Appended {len(new_sents)} sentences to corpus.")

    if newly_processed:
        with open(PROCESSED_LOG, "a", encoding="utf-8") as f:
            for name in newly_processed:
                f.write(name + "\n")
        print(f"Marked {len(newly_processed)} files as processed.")


if __name__ == "__main__":
    main()
