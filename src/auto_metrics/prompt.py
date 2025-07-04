"""
Functions to generate a prompt for rating articles using METRICS.
"""

from .metrics import Item, Condition
from .logger import logger

BASE_PROMPT = """
# Instructions
You are an expert radiologist with decades of experience in developing and implementing clinical artificial intelligence.
You have to offer ratings to a scientific article of clinical importance at the end of this prompt according to a set of criteria (items).
You must answer carefully and thoughtfully, considering the context of the article and your expertise.
Be extremely thorough and conservative with your answers as these tools are supposed to be deployed in the clinic.

# Evaluation
## Metrics definition
There are 30 items in total and each item is grouped into one of 9 categories.
There are, additionally, 5 conditions which define whether some item should be filled or not.
The 5 Conditions are defined below under "# Conditions". A short explanation is provided for each.
The 30 items are defined below under "# Items". Each is grouped under its respective category. A short explanation is provided for each.

## Rating Rubric
No: no evidence that this item is being followed in this publication
Yes: evidence that this item is being followed in this publication
n/a: not applicable
Reason: a short explanation for each ranking

# Input format
The article text is provided below under "# Article text". Anything outside of this text should not be evaluated.

# Output format
You have to output a JSON file with the following structure:
- a summary of the article accurately representing the main conclusion of the article
- the answers for conditions (Yes, No) (described under "# Conditions") and a short explanation for your decision
- the ratings (Yes, No or n/a) for each item (described under "# Items") and a short explanation for your decision
"""

REASONING_PROMPT = """
# Instructions
You are an expert radiologist with decades of experience in developing and implementing clinical artificial intelligence.
You have to offer ratings to a scientific article of clinical importance at the end of this prompt according to a set of criteria (items).
You must answer carefully and thoughtfully, considering the context of the article and your expertise.
Be extremely thorough and conservative with your answers as these tools are supposed to be deployed in the clinic.

# Evaluation
## Metrics definition
There are 30 items in total and each item is grouped into one of 9 categories.
There are, additionally, 5 conditions which define whether some item should be filled or not.
The 5 Conditions are defined below under "# Conditions". A short explanation is provided for each.
The 30 items are defined below under "# Items". Each is grouped under its respective category. A short explanation is provided for each.

## Rating Rubric
- Criteria description ("criteria_description"): a short description of the criteria used for the rating. This is used to remind you of the criteria
- Reasoning trace ("reasoning"): the reasoning trace for each rating. Be as extensive as you need and provide the adequate reasoning for each rating. It should be immediately clear to the reader why each rating was provided.
- Rating ("rating"): the rating for each item (i.e. No: no evidence that this item is being followed in this publication; Yes: evidence that this item is being followed in this publication; n/a: not applicable)

# Input format
The article text is provided below under "# Article text". Anything outside of this text should not be evaluated.

# Output format
You have to output a JSON file with the following structure:
- a list of items with a simplified description of the criteria used for the rating (criteria_description), the reasoning trace for the answer provided in "rating" ("reasoning") and the rating for the item ("rating"). Each Item is described under "# Items".
- a list of conditions with a simplified description of the criteria used for the rating (criteria_description), the reasoning trace for the answer provided in "rating" ("reasoning") and the rating for the condition ("rating"). Each Condition is described under "# Conditions".
- Summary: a summary of the article accurately representing the main conclusion of the article
"""


def format_generic(
    identifier: str,
    number: int,
    description: str,
    comment: str,
    name: str | None = None,
) -> str:
    """
    Generic formatting for items and conditions.

    Args:
        identifier (str): The identifier for the item or condition (e.g. "Item" or "Condition").
        number (int): The number of the item or condition.
        description (str): The description of the item or condition.
        comment (str): The comment of the item or condition.
        name (str, optional): The name of the item or condition.

    Returns:
        str: The formatted string.
    """
    if name is None:
        return f"* {identifier}{number}: {description} - {comment}"
    else:
        return f"* {identifier}{number}_{name}: {description} - {comment}"


def make_prompt(
    item_list: dict[str, list[Item]],
    conditions: list[Condition],
    prompt_type: str = "default",
    with_names: bool = False,
) -> str:
    """
    Make a prompt for rating articles using METRICS.

    Args:
        item_list (dict[str, list[Item]]): The list of items (as ``Item``
            objects) grouped by section.
        conditions (list[Condition]): The list of conditions (as ``Condition``
            objects).
        prompt_type (str, optional): The type of prompt to generate. Defaults to
            "default".
        with_names (bool, optional): Whether to include names in the prompt.
            Defaults to False.

    Returns:
        str: The prompt.
    """
    if prompt_type == "default":
        prompt_complete = BASE_PROMPT + "\n"
    elif prompt_type == "reasoning":
        prompt_complete = REASONING_PROMPT + "\n"
    else:
        raise ValueError(f"Unknown prompt type: {prompt_type}")

    if len(conditions) > 0:
        prompt_complete += "# Conditions\n\n"
        for condition in conditions:
            if with_names is True and condition.name is None:
                logger.warning(
                    f"with_names set to True but condition {condition.number} has no name"
                )
            prompt_complete += format_generic(
                "Condition",
                condition.number,
                condition.description,
                condition.comment,
                name=condition.name if with_names else None,
            )
            prompt_complete += "\n"

    prompt_complete += "\n\n# Items\n\n"
    section_order = sorted(
        item_list.keys(),
        key=lambda k: min([item.number for item in item_list[k]]),
    )
    for section in section_order:
        prompt_complete += f"## {section}\n\n"
        for item in item_list[section]:
            if with_names is True and item.name is None:
                logger.warning(
                    f"with_names set to True but item {item.number} has no name"
                )
            prompt_complete += format_generic(
                "Item",
                item.number,
                item.description,
                item.comment,
                name=item.name if with_names else None,
            )
            if item.condition is not None:
                condition_text = " and ".join([f"{c}" for c in item.condition])
                prompt_complete += (
                    f' Answer only if Condition {condition_text} are "yes".'
                )
            prompt_complete += "\n"
        prompt_complete += "\n"
    return prompt_complete


if __name__ == "__main__":
    import argparse
    from metrics import load_config

    parser = argparse.ArgumentParser()

    parser.add_argument("--config_path", default="config.yaml")

    args = parser.parse_args()

    items, conditions = load_config(args.config_path)
    print(make_prompt(items, conditions))
