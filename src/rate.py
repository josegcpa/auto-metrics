from pydantic import ValidationError


if __name__ == "__main__":
    import os
    import argparse
    import json
    import time
    import logging
    from pathlib import Path

    from .logger import logger
    from .metrics import load_config
    from .ratings import export_model_to_json
    from .ratings import dynamically_generate_model
    from .prompt import make_prompt

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--article_path",
        type=str,
        required=True,
        help="Path to the article text file",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="Path to the output file",
    )
    parser.add_argument(
        "--config_path",
        type=str,
        default="config.yaml",
        help="Path to the config file",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it exists",
    )
    parser.add_argument(
        "--local_model",
        type=str,
        default=None,
        help="Local model to use for rating. Format: provider:model_str. "
        "If not provided, Gemini will be used. "
        "Only ollama and huggingface are supported for provider.",
    )
    parser.add_argument(
        "--prompt_type",
        type=str,
        default="default",
        help="Type of prompt to use",
        choices=["default", "skip_reasons"],
    )
    parser.add_argument(
        "--with_names",
        action="store_true",
        help="Whether to include item names in the prompt "
        "(improves results for local models)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode. Raises error rather than warning when JSON is not valid",
        default=False,
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=None,
        help="Maximum number of tokens. For open/local models.",
    )
    args = parser.parse_args()

    if args.verbose is True:
        logger.setLevel(logging.DEBUG)

    with open(args.article_path) as f:
        article_text = f.read()

    if args.output_path is not None and not args.overwrite:
        if os.path.exists(args.output_path):
            logger.info(
                "Output file already exists. Use --overwrite to overwrite."
            )
            exit(0)

    item_list, conditions, flat_items = load_config(args.config_path)
    prompt = make_prompt(
        item_list,
        conditions,
        prompt_type=args.prompt_type,
        with_names=args.with_names,
    )

    data_model = dynamically_generate_model(
        flat_items,
        conditions,
        skip_reasons=args.prompt_type == "skip_reasons",
        with_names=args.with_names,
    )

    start_time = time.time()
    if args.local_model is None:
        logger.info("Using Gemini")
        from .request_utils.gemini_request import query_model

        response = query_model(
            prompt=prompt,
            article_text=article_text,
            data_model=data_model,
        )
    else:
        split_model = args.local_model.split(":")
        provider, model_str = split_model[0], ":".join(split_model[1:])
        logger.info(f"Using {model_str} from {provider}")
        if provider == "ollama":
            from .request_utils.ollama_request import query_model

            response = query_model(
                prompt=prompt,
                article_text=article_text,
                data_model=export_model_to_json(data_model),
                model_str=model_str,
                max_tokens=args.max_tokens,
            )
        elif provider == "huggingface":
            from .request_utils.huggingface_request import query_model

            response = query_model(
                prompt=prompt,
                article_text=article_text,
                data_model=data_model,
                model_str=model_str,
                max_tokens=args.max_tokens,
            )
        else:
            raise ValueError(
                "Providers are restricted to 'ollama' and 'huggingface' (uses outlines)"
            )

    verbose_eval = response
    try:
        json_response = data_model.model_validate_json(
            verbose_eval
        ).model_dump(mode="json")
        error = None
    except ValidationError as e:
        if args.strict:
            raise e
        logger.warning(
            f"Failed to parse response as JSON:\n{str(e)}.\nExiting"
        )
        json_response = {}
        error = str(e)

    json_response["metadata"] = {
        "prompt": prompt,
        "prompt_path": None,  # placeholder
        "config_path": args.config_path,
        "article_text": article_text,
        "article_text_path": args.article_path,
        "model": args.local_model,
        "error": error,
        "elapsed_time": time.time() - start_time,
    }

    if args.output_path is None:
        print(verbose_eval)
    else:
        logger.info(f"Exporting ratings to {args.output_path}")
        Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_path, "w") as f:
            json.dump(json_response, f, indent=2)
