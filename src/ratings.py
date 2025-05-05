from enum import Enum
from pydantic import create_model
from pydantic import BaseModel, Field
from .metrics import Item, Condition
from .logger import logger


class RatingEnum(Enum):
    yes = "yes"
    no = "no"


class RatingWithNAEnum(Enum):
    yes = "yes"
    no = "no"
    na = "n/a"


class Rating(BaseModel):
    rating: RatingEnum
    reason: str


class RatingWithNA(BaseModel):
    rating: RatingWithNAEnum
    reason: str


class RatingReasoning(BaseModel):
    criteria_description: str
    reasoning: list[str]
    rating: RatingEnum


class RatingWithNAReasoning(BaseModel):
    criteria_description: str
    reasoning: list[str]
    rating: RatingWithNAEnum


class RatingNoReason(BaseModel):
    rating: RatingEnum


class RatingWithNANoReason(BaseModel):
    rating: RatingWithNAEnum


class Metrics(BaseModel):
    Summary: str
    Item1: Rating
    Item2: Rating
    Item3: Rating
    Item4: Rating
    Item5: Rating
    Item6: Rating
    Item7: Rating
    Condition1: Rating
    Condition2: Rating
    Item8: RatingWithNA
    Item9: RatingWithNA
    Item10: RatingWithNA
    Condition3: Rating
    Item11: Rating
    Item12: RatingWithNA
    Item13: Rating
    Condition4: Rating
    Condition5: Rating
    Item14: RatingWithNA
    Item15: RatingWithNA
    Item16: RatingWithNA
    Item17: RatingWithNA
    Item18: Rating
    Item19: Rating
    Item20: Rating
    Item21: Rating
    Item22: Rating
    Item23: Rating
    Item24: Rating
    Item25: Rating
    Item26: Rating
    Item27: Rating
    Item28: Rating
    Item29: Rating
    Item30: Rating


def dynamically_generate_model(
    items: list[Item],
    conditions: list[Condition] | None = None,
    with_names: bool = False,
    reasoning: bool = False,
):
    logger.info(
        f"Generating answers with {len(items)} items, {len(conditions)} conditions, "
        f"with_names={with_names}, reasoning={reasoning}"
    )
    if reasoning:
        rating = RatingReasoning
        rating_na = RatingWithNANoReason
    else:
        rating = Rating
        rating_na = RatingWithNA
    model = {}
    if conditions is not None:
        for condition in conditions:
            key = (
                f"Condition{condition.number}_{condition.name}"
                if with_names
                else f"Condition{condition.number}"
            )
            model[key] = (
                rating,
                Field(
                    description=f"{condition.description}\n{condition.comment}"
                ),
            )
    for item in items:
        key = (
            f"Item{item.number}_{item.name}"
            if with_names
            else f"Item{item.number}"
        )
        model[key] = (
            rating_na if item.condition else rating,
            Field(description=f"{item.description}\n{item.comment}"),
        )
    model["Summary"] = (str, Field(description="Summary of the article"))
    return create_model("Criteria", **model)


def export_model_to_json(data_model: BaseModel):
    def dig_dict(d, ref_dict: dict):
        if isinstance(d, dict):
            if "enum" in d:
                d["type"] = "string"
            if "$ref" in d:
                ref = d["$ref"]
                return dig_dict(ref_dict[ref], ref_dict)
            return {k: dig_dict(v, ref_dict) for k, v in d.items()}
        elif isinstance(d, list):
            return [dig_dict(v, ref_dict) for v in d]
        else:
            return d

    model_schema_with_refs = data_model.model_json_schema()
    refs_dict = {
        "#/$defs/" + k: model_schema_with_refs["$defs"][k]
        for k in model_schema_with_refs["$defs"]
    }
    model_schema = dig_dict(model_schema_with_refs, refs_dict)
    del model_schema["$defs"]
    return model_schema


def get_weights(flat_items: list[Item]):
    return {f"Item{item.number}": item.weight for item in flat_items}


if __name__ == "__main__":
    import json

    print(json.dumps(export_model_to_json(Metrics), indent=2))
