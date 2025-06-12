from dataclasses import dataclass

@dataclass
class Parameters:
    TEMPERATURE = 0.0
    TOP_P = 0.001
    TOP_K = 5
    SEED = 42
    FREQUENCY_PENALTY = 0.0
    PRESENCE_PENALTY = 0.0