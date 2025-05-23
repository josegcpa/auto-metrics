import yaml
from pydantic import BaseModel
from .logger import logger


class Item(BaseModel):
    number: int
    description: str
    comment: str
    name: str | None = None
    condition: list[int] | None = None
    weight: float | None = None


class Condition(BaseModel):
    number: int
    description: str
    comment: str
    name: str | None = None


def load_config(
    config_path: str = "config.yaml",
) -> tuple[str, dict[str, list[Item]], list[Condition]]:
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
