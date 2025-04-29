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

    from metrics import load_config
    from ratings import export_model_to_json
    from prompt import make_prompt

    parser = argparse.ArgumentParser()
    parser.add_argument("--article_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--config_path", type=str, default="config.yaml")
    parser.add_argument("--local_model", type=str, default=None)
    parser.add_argument("--skip_reasons", action="store_true")
    args = parser.parse_args()

    with open(args.article_path) as f:
        article_text = f.read()

    if args.output_path is not None and not args.overwrite:
        if os.path.exists(args.output_path):
            print("Output file already exists. Use --overwrite to overwrite.")
            exit(0)

    item_list, conditions, flat_items = load_config(args.config_path)
    prompt = make_prompt(item_list, conditions, skip_reasons=args.skip_reasons)

    data_model = dynamically_generate_model(
        flat_items, conditions, skip_reasons=args.skip_reasons
    )

    start_time = time.time()
    if args.local_model is None:
        from request_utils.gemini_request import query_model

        response = query_model(prompt.format(article=article_text), data_model)
    else:
        split_model = args.local_model.split(":")
        provider, model_str = split_model[0], ":".join(split_model[1:])
        if provider == "ollama":
            from request_utils.ollama_request import query_model

            response = query_model(
                query=prompt.format(article=article_text),
                data_model=export_model_to_json(data_model),
                model_str=model_str,
            )
        elif provider == "huggingface":
            from request_utils.huggingface_request import query_model

            response = query_model(
                prompt.format(article=article_text), data_model, model_str
            )
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
