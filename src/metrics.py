import yaml
from pydantic import BaseModel


class Item(BaseModel):
    item_number: int
    item_description: str
    item_comment: str
    condition: list[int] | None = None


class Condition(BaseModel):
    condition_number: int
    condition_description: str
    condition_comment: str


def load_config(
    config_path: str = "config.yaml",
) -> tuple[str, dict[str, list[Item]], list[Condition]]:
    with open(config_path) as o:
        data = yaml.safe_load(o)
    conditions = sorted(
        [Condition(**x) for x in data["conditions"]],
        key=lambda condition: condition.condition_number,
    )
    items = {k: [Item(**x) for x in data["items"][k]] for k in data["items"]}
    return items, conditions


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--config_path", default="config.yaml")

    args = parser.parse_args()

    print(load_config(args.config_path))
