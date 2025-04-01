from metrics import Item, Condition

BASE_PROMPT = """
# Instructions
You are an expert radiologist with decades of experience in developing and implementing clinical artificial intelligence.
You have to offer ratings to a scientific article of clinical importance at the end of this prompt according to a set of criteria.
You must answer carefully and thoughtfully, considering the context of the article and your expertise.
Be extremely thorough and conservative with your answers as these tools are supposed to be deployed in the clinic.

# Evaluation
## Metrics definition
There are 30 criteria in total and each criterion is grouped into one of 9 categories.
There are, additionally, 5 conditions which define whether some criterion should be filled or not.
The 5 Conditions are defined below under "## Conditions". A short explanation is provided for each.
The 30 criteria are defined below under "## Criteria". Each is grouped under its respective category. A short explanation is provided for each.

## Rating Rubric
No: no evidence that this criterion is being followed in this publication
Yes: evidence that this criterion is being followed in this publication
n/a: not applicable
Reason: a short explanation for each ranking

# Input format
The article text is provided below under "# Article text". Anything outside of this text should not be evaluated.

# Output format
You have to output:
- a summary of the article accurately representing the main conclusion of the article
- the answers for conditions (Yes, No) and a short explanation for your decision
- the ratings (Yes, No or n/a) for each criterion and a short explanation for your decision
"""


def format_generic(
    identifier: str, number: int, description: str, comment: str
) -> str:
    return f"* {identifier} {number}: {description} - {comment}"


def make_prompt(
    item_list: dict[str, list[Item]],
    conditions: list[Condition],
) -> str:
    prompt_complete = BASE_PROMPT + "\n"

    prompt_complete += "## Conditions\n\n"
    for condition in conditions:
        prompt_complete += format_generic(
            "Condition",
            condition.condition_number,
            condition.condition_description,
            condition.condition_comment,
        )
        prompt_complete += "\n"

    prompt_complete += "\n\n## Criteria\n\n"
    section_order = sorted(
        item_list.keys(),
        key=lambda k: min([item.item_number for item in item_list[k]]),
    )
    for section in section_order:
        prompt_complete += f"### {section}\n"
        for item in item_list[section]:
            prompt_complete += format_generic(
                "Item",
                item.item_number,
                item.item_description,
                item.item_comment,
            )
            if item.condition is not None:
                condition_text = " and ".join([f"{c}" for c in item.condition])
                prompt_complete += (
                    f' Answer only if Condition {condition_text} are "yes".'
                )
            prompt_complete += "\n"
        prompt_complete += "\n"
    prompt_complete += "\n# Article text\n\n{article}"
    return prompt_complete


if __name__ == "__main__":
    import argparse
    from metrics import load_config

    parser = argparse.ArgumentParser()

    parser.add_argument("--config_path", default="config.yaml")

    args = parser.parse_args()

    items, conditions = load_config(args.config_path)
    print(make_prompt(items, conditions))
