# Auto-METRICS

This repository features code allowing for the automatic quality control of radiomics research. In short, it makes use of Gemini to generate a report on the quality of a radiomics study following the guidelines for the [METhodological RadiomICs Score (METRICS)](https://insightsimaging.springeropen.com/articles/10.1186/s13244-023-01572-w).

This code is part of the paper "Auto-METRICS: LLM-assisted scientific quality control for radiomics research".

## Usage

We use [`uv`](https://docs.astral.sh/uv/) to manage the dependencies and run everything, so running this software should be fairly straightforward. To rate a given manuscript all you have to do is run:

```bash
uv run python src/rate.py --input_path <path_to_manuscript_in_txt> --output_path <path_to_output_json> --config_path <path_to_config_yaml>
```

`uv` does a good job at managing the dependencies at runtime so it should be easy to install/run everything.

The input manuscript should be provided as a `.txt` file, and the output will be a `.json` file containing the ratings. The configuration YAML files (two examples are provided in [config.yaml](https://github.com/josegcpa/auto-metrics/blob/main/config.yaml) and in [config-enhanced.yaml](https://github.com/josegcpa/auto-metrics/blob/main/config-enhanced.yaml)) specify each rating item and whether it depends on specific conditions. This allows for changes in rating systems as they might be refined throughout the years.

## User interface

Not everyone likes or feels comfortable using the command line, so we have provided an easily usable interface for Auto-METRICS available [here](https://autometrics.josegcpa.net/). This is automatically dispatched with every update to the code repository through Github Actions and is hosted using Netlify.

## Expansions

For now we are not planning any expansions to this methodology, but if you find any issues or have any suggestions, please open an issue or contact us.

## Citation

de Almeida JG, Papanikolaou, N (2025) Auto-METRICS: LLM-assisted scientific quality control for radiomics research. medRxiv [Preprint] doi: [10.1101/2025.04.22.25325873](https://www.medrxiv.org/content/10.1101/2025.04.22.25325873v1)