SOURCE_DIR = "src/static_app_templates"

if __name__ == "__main__":
    import os
    import json
    from ratings import export_model_to_json
    from prompt import make_prompt
    from metrics import load_config

    import argparse

    parser = argparse.ArgumentParser(description="Generate static app")
    parser.add_argument("--config_path", default="config.yaml")
    parser.add_argument("--output_dir", default="static_app")
    args = parser.parse_args()

    items, conditions = load_config(args.config_path)
    input_prompt = make_prompt(items, conditions)
    output_data_model = export_model_to_json()

    with open(f"{SOURCE_DIR}/main.js", "r") as f:
        main_js = f.read()

    js_file = main_js.replace(
        '"!PROMPT"', input_prompt.replace("{article}", "")
    ).replace('"!RESPONSE_SCHEMA"', json.dumps(output_data_model))

    with open(f"{SOURCE_DIR}/index.html", "r") as f:
        main_html = f.read().replace(
            '<script src="static/js/main.js"></script>',
            f'<script src="main.js"></script>',
        )

    os.makedirs(args.output_dir, exist_ok=True)
    with open(f"{args.output_dir}/index.html", "w") as f:
        f.write(main_html)
    with open(f"{args.output_dir}/main.js", "w") as f:
        f.write(js_file)
