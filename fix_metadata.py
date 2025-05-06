import os
import json
from pathlib import Path
from src.metrics import load_config
from src.prompt import make_prompt


def fix_meta(path: str):
    info = path.split(os.sep)
    config_file = (
        "config.yaml" if info[0] == "ratings" else "config-enhanced.yaml"
    )
    model = info[1]
    article_name = info[-1].replace(".json", "")
    article_path = str(
        next(
            Path("article-text").rglob(
                f"*{article_name}*".replace("[", "*").replace("]", "*")
            )
        )
    )
    items, conditions, flat_items = load_config(config_file)
    prompt = make_prompt(
        items, conditions, flat_items, with_names=model != "gemini"
    )
    with open(path) as f:
        d = json.load(f)
    with open(article_path) as f:
        article_text = f.read()
    if "elapsed_time" in d:
        d["metadata"] = {
            "prompt": prompt,
            "prompt_path": None,  # placeholder
            "config_path": config_file,
            "article_text": article_text,
            "article_text_path": article_path,
            "model": model if model != "gemini" else None,
            "error": None,
            "elapsed_time": d["elapsed_time"],
        }
        del d["elapsed_time"]
        print(f"Saved metadata to {path}")
    with open(path, "w") as f:
        json.dump(d, f, indent=2)


for path in Path("ratings").rglob("*json"):
    fix_meta(str(path))

for path in Path("ratings_improved").rglob("*json"):
    fix_meta(str(path))
