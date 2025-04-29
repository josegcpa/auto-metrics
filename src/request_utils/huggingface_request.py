import outlines
import torch
from tqdm import tqdm
from pydantic import BaseModel
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
from .parameters import SEED

if torch.cuda.is_available():
    device = "cuda"
elif torch.mps.is_available():
    device = "mps"
else:
    device = "cpu"

set_seed(SEED)


def query_model(query: str, data_model: BaseModel, model_str: str):
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
    sampling_parameters = SamplingParameters(sampler="greedy")

    outlines_model = Transformers(model=model, tokenizer=tokenizer)
    response_stream = outlines_model.stream(
        query,
        generation_parameters=GenerationParameters(
            max_tokens=None, stop_at=None, seed=SEED
        ),
        logits_processor=processor,
        sampling_parameters=sampling_parameters,
    )
    response = ""
    for content in tqdm(response_stream):
        response += content

    return response
