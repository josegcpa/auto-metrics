"""
Contains the data models for generic metrics.
"""

import yaml
from pydantic import BaseModel, field
from .logger import logger


class Item(BaseModel):
    """
    Data model for a metric item.
    """
    number: int = field(description="Item number")
    description: str = field(description="Item description")
    comment: str = field(description="Item comment with clarification")
    name: str | None = field(description="Item name", default=None)
    condition: list[int] | None = field(
        description="Item condition (only if it depends on a specific condition)",
        default=None,
    )
    weight: float | None = field(description="Item weight", default=None)


class Condition(BaseModel):
    """
    Data model for conditions (define whether items should be considered).
    """
    number: int = field(description="Condition number")
    description: str = field(description="Condition description")
    comment: str = field(description="Condition comment with clarification")
    name: str | None = field(description="Condition name", default=None)


def load_config(
    config_path: str = "config.yaml",
) -> tuple[str, dict[str, list[Item]], list[Condition]]:
    """
    Loads the configuration from a YAML file. In the YAML file, two main keys
    are expected:

        - "items": these should be partitioned into sections (e.g., "Study Design",
        "Feature Extraction", etc.) and within each section each item should be
        defined by its ``number``, a ``description`` (loose description of the
        item) and a ``comment`` (detailed description of the item). Additional
        optional fields include its ``name``, the ``condition`` it depends on (as
        a list of numbers) and its ``weight``.

        - "conditions": these should be defined by its ``number``, a
        ``description`` (loose description of the condition) and a ``comment``
        (detailed description of the condition). Additional optional fields
        include its ``name``.

    Args:
        config_path: Path to the YAML file.

    Returns:
        A tuple containing the items, the conditions, and a flattened version
            of the items.
    """
    logger.info(f"Loading configuration from {config_path}")
    with open(config_path) as o:
        data = yaml.safe_load(o)
    conditions = sorted(
        [Condition(**x) for x in data["conditions"]],
        key=lambda condition: condition.number,
    )
    items = {}
    flat_items = []
    for k in data["items"]:
        items[k] = [Item(**x) for x in data["items"][k]]
        flat_items.extend(items[k])
    return items, conditions, flat_items


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--config_path", default="config.yaml")

    args = parser.parse_args()

    print(load_config(args.config_path))
