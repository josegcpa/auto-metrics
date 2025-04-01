if __name__ == "__main__":
    import os
    import argparse
    from pathlib import Path
    from google import genai
    from google.genai import types

    from metrics import load_config
    from ratings import Metrics
    from prompt import make_prompt

    parser = argparse.ArgumentParser()
    parser.add_argument("--article_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--config_path", type=str, default="config.yaml")
    args = parser.parse_args()

    with open(args.article_path) as f:
        article_text = f.read()

    if args.output_path is not None and not args.overwrite:
        if os.path.exists(args.output_path):
            print("Output file already exists. Use --overwrite to overwrite.")
            exit(0)

    item_list, conditions = load_config(args.config_path)
    prompt = make_prompt(item_list, conditions)

    config = types.GenerateContentConfig(
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=Metrics,
    )

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    chat = client.chats.create(model="gemini-2.0-flash")

    response = chat.send_message(
        message=prompt.format(article=article_text), config=config
    )
    verbose_eval = response.text

    if args.output_path is None:
        print(verbose_eval)
    else:
        Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_path, "w") as f:
            f.write(verbose_eval)
