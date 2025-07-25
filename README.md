# Auto-METRICS

This repository features code allowing for the automatic quality control of radiomics research. In short, it makes use of Gemini to generate a report on the quality of a radiomics study following the guidelines for the [METhodological RadiomICs Score (METRICS)](https://insightsimaging.springeropen.com/articles/10.1186/s13244-023-01572-w).

This code is part of the paper "Auto-METRICS: LLM-assisted scientific quality control for radiomics research".

## Usage

We use [`uv`](https://docs.astral.sh/uv/) to manage the dependencies and run everything, so running this software should be fairly straightforward. 

### Use with Gemini (default)

To rate a given manuscript with Gemini all you have to do is run:

```bash
uv run rate --article_path <path_to_manuscript_in_txt> --output_path <path_to_output_json> --config_path <path_to_config_yaml>
```

`uv` does a good job at managing the dependencies at runtime so it should be easy to install/run everything.

The input manuscript should be provided as a `.txt` file, and the output will be a `.json` file containing the ratings. The configuration YAML files (two examples are provided in [config.yaml](https://github.com/josegcpa/auto-metrics/blob/main/config.yaml) and in [config-enhanced.yaml](https://github.com/josegcpa/auto-metrics/blob/main/config-enhanced.yaml)) specify each rating item and whether it depends on specific conditions. This allows for changes in rating systems as they might be refined throughout the years.

### Use with Ollama models

To run this with Ollama models, simply add the local model flag `--local_model` to the command. Through this, you can specify an Ollama model (with `ollama:<model_identifier>`). Importantly, if you want to run Ollama models you should keep in mind that [Ollama](https://ollama.com/) should be installed and running. Models have to be pulled from the Ollama repository (`ollama pull <model_identifier>`) prior to being used. 

**Note:** We recommend running Ollama models with the `--with_names` option. This will add name pseudo-name identifiers to each item and leads to better results. From our experience, structured generation was not reliable without this as item names were quite similar.

### Use with HuggingFace models

To use HuggingFace please add the `--extra huggingface` option to your commands as this will ensure that HuggingFace dependencies are downloaded (i.e. `uv run --extra huggingface rate ...`).

Then you can use it similarly to the Ollama models (with `--local_model`) but with a HuggingFace model (with `huggingface:<model_identifier>`). This does not require pulling models from the repository, but tends to be more resource intensive (from our experience).

**Important note:** we did not validate how Auto-METRICS works with HuggingFace models. It produces an output similar to what is produced by the other routes, but whether that output is reliable has not been confirmed.

### Short note on guided generation with local models

For both Ollama and HuggingFace models, structured generation is supported - this is what allows us to have any model produce a JSON. However, they both use slightly different frameworks: 

- Ollama uses GBNF grammars (as implemented in the [llama.cpp](https://github.com/ggml-org/llama.cpp) project)
- The HuggingFace framework we have implemented leverages [outlines.txt](https://github.com/dottxt-ai/outlines). This supports more generic structuring with regular expressions (more information on this: [Efficient Guided Generation for Large Language Models](https://arxiv.org/pdf/2307.09702)). 

For the use cases at hand they are practically equivalent as they simply constrain, at each sampling step, which tokens can be generated and we do not use any regular expressions.

## User interface

Not everyone likes or feels comfortable using the command line, so we have provided an easily usable interface for Auto-METRICS available [here](https://autometrics.josegcpa.net/). This is automatically dispatched with every update to the code repository through Github Actions and is hosted using Netlify.

## Expansions

For now we are not planning any expansions to this methodology, but if you find any issues or have any suggestions, please open an issue or contact us.

## Citation

de Almeida JG, Papanikolaou, N (2025) Auto-METRICS: LLM-assisted scientific quality control for radiomics research. medRxiv [Preprint] doi: [10.1101/2025.04.22.25325873](https://www.medrxiv.org/content/10.1101/2025.04.22.25325873v1)