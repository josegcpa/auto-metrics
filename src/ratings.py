from enum import Enum
from pydantic import BaseModel


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


class Metrics(BaseModel):
    Summary: str
    Condition1: Rating
    Condition2: Rating
    Condition3: Rating
    Condition4: Rating
    Condition5: Rating
    Item1: Rating
    Item2: Rating
    Item3: Rating
    Item4: Rating
    Item5: Rating
    Item6: Rating
    Item7: Rating
    Item8: RatingWithNA
    Item9: RatingWithNA
    Item10: RatingWithNA
    Item11: Rating
    Item12: RatingWithNA
    Item13: Rating
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


SCORES = {
    "Item1": 0.0368,
    "Item2": 0.0735,
    "Item3": 0.0919,
    "Item4": 0.0438,
    "Item5": 0.0292,
    "Item6": 0.0438,
    "Item7": 0.0292,
    "Item8": 0.0337,
    "Item9": 0.0225,
    "Item10": 0.0112,
    "Item11": 0.0622,
    "Item12": 0.0311,
    "Item13": 0.0415,
    "Item14": 0.0200,
    "Item15": 0.0200,
    "Item16": 0.0300,
    "Item17": 0.0200,
    "Item18": 0.0599,
    "Item19": 0.0300,
    "Item20": 0.0352,
    "Item21": 0.0234,
    "Item22": 0.0176,
    "Item23": 0.0117,
    "Item24": 0.0293,
    "Item25": 0.0176,
    "Item26": 0.0375,
    "Item27": 0.0749,
    "Item28": 0.0075,
    "Item29": 0.0075,
    "Item30": 0.0075,
}
