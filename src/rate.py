from ratings import dynamically_generate_model


TEMPERATURE = 0.0
TOP_P = 0.001
SEED = 42

if __name__ == "__main__":
    import os
    import argparse
    import json
    import time
    from pathlib import Path
    from tqdm import tqdm

    from metrics import load_config
    from ratings import export_model_to_json
    from prompt import make_prompt

    parser = argparse.ArgumentParser()
    parser.add_argument("--article_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--config_path", type=str, default="config.yaml")
    parser.add_argument("--local_model", type=str, default=None)
    args = parser.parse_args()

    with open(args.article_path) as f:
        article_text = f.read()

    if args.output_path is not None and not args.overwrite:
        if os.path.exists(args.output_path):
            print("Output file already exists. Use --overwrite to overwrite.")
            exit(0)

    item_list, conditions, flat_items = load_config(args.config_path)
    prompt = make_prompt(item_list, conditions)

    data_model = dynamically_generate_model(flat_items, conditions)

    start_time = time.time()
    if args.local_model is None:
        from google import genai
        from google.genai.types import GenerateContentConfig

        config = GenerateContentConfig(
            temperature=TEMPERATURE,
            top_p=TOP_P,
            seed=SEED,
            response_mime_type="application/json",
            response_schema=data_model,
        )

        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        chat = client.chats.create(model="gemini-2.0-flash-001")

        response = chat.send_message(
            message=prompt.format(article=article_text), config=config
        )
        response = response.text
    else:
        split_model = args.local_model.split(":")
        provider, model_str = split_model[0], ":".join(split_model[1:])
        if provider == "ollama":
            from ollama import Client

            client = Client()
            response_stream = client.generate(
                prompt=prompt.format(article=article_text),
                model=model_str,
                options={
                    "top_p": TOP_P,
                    "seed": SEED,
                    "temperature": TEMPERATURE,
                },
                format=export_model_to_json(data_model),
                stream=True,
            )
            response = ""
            for content in tqdm(response_stream):
                response += content["response"]
        elif provider == "huggingface":
            import outlines
            import torch
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
            )
            from outlines.models.transformers import Transformers
            from outlines.generate.api import (
                GenerationParameters,
                SamplingParameters,
            )
            from transformers import set_seed

            if torch.cuda.is_available():
                device = "cuda"
            elif torch.mps.is_available():
                device = "mps"
            else:
                device = "cpu"

            set_seed(SEED)

            model = AutoModelForCausalLM.from_pretrained(
                model_str,
                device_map=device,
                torch_dtype="auto",
                trust_remote_code=True,
            )
            tokenizer = AutoTokenizer.from_pretrained(model_str)
            outlines_tokenizer = outlines.models.TransformerTokenizer(tokenizer)

            processor = outlines.processors.JSONLogitsProcessor(
                data_model, tokenizer=outlines_tokenizer
            )
            sampling_parameters = SamplingParameters(
                sampler="greedy",
                top_p=TOP_P,
                temperature=TEMPERATURE + 1e-6,
            )

            outlines_model = Transformers(model=model, tokenizer=tokenizer)
            response_stream = outlines_model.stream(
                prompt.format(article=article_text),
                generation_parameters=GenerationParameters(
                    max_tokens=None, stop_at=None, seed=SEED
                ),
                logits_processor=processor,
                sampling_parameters=sampling_parameters,
            )
            response = ""
            for content in tqdm(response_stream):
                response += content
        else:
            raise ValueError(
                "Providers are restricted to 'ollama' and 'huggingface' (uses outlines)"
            )

    verbose_eval = response
    json_response = data_model.model_validate_json(verbose_eval).model_dump(
        mode="json"
    )
    json_response["elapsed_time"] = time.time() - start_time

    if args.output_path is None:
        print(verbose_eval)
    else:
        Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_path, "w") as f:
            json.dump(json_response, f, indent=2)
