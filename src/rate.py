if __name__ == "__main__":
    import os
    import argparse
    import json
    import time
    from pathlib import Path
    from tqdm import tqdm
    from ollama import Client
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
    parser.add_argument("--ollama_model", type=str, default=None)
    args = parser.parse_args()

    with open(args.article_path) as f:
        article_text = f.read()

    if args.output_path is not None and not args.overwrite:
        if os.path.exists(args.output_path):
            print("Output file already exists. Use --overwrite to overwrite.")
            exit(0)

    item_list, conditions = load_config(args.config_path)
    prompt = make_prompt(item_list, conditions)

    start_time = time.time()
    if args.ollama_model is None:
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
        response = response.text
    else:
        client = Client()
        response_stream = client.chat(
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(article=article_text),
                },
            ],
            model=args.ollama_model,
            options={"temperature": 0.0},
            format=Metrics.model_json_schema(),
            stream=True,
        )
        response = ""
        for content in tqdm(response_stream):
            response += content["message"]["content"]

    verbose_eval = response
    json_response = Metrics.model_validate_json(verbose_eval).model_dump(
        mode="json"
    )
    json_response["elapsed_time"] = time.time() - start_time

    if args.output_path is None:
        print(verbose_eval)
    else:
        Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_path, "w") as f:
            json.dump(json_response, f, indent=2)
