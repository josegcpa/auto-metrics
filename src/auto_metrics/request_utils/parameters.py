from dataclasses import dataclass

@dataclass
class Parameters:
    """
    Parameters for the requests.
    """
    TEMPERATURE: float = 0.0
    TOP_P: float = 0.001
    TOP_K: int = 5
    SEED: int = 42
    FREQUENCY_PENALTY: float = 0.0
    PRESENCE_PENALTY: float = 0.0
