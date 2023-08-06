from pydantic import (
    BaseModel, validator, root_validator, AnyUrl
)

from typing import Optional, Dict, List


def coord0_less_than_coord1(coord0, coord1):
    if coord0 >= coord1:
        return False
    return True


class BoundingBox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float
    bbox_class: str

    @root_validator
    def between_zero_and_one(cls, values):
        for key in values:
            if key != "bbox_class":
                if values[key] > 1 or values[key] < 0:
                    raise ValueError(
                        f"{key} must be greater or equal to zero and less than or equal to one."
                    )
        return values

    @root_validator
    def x0_less_than_x1(cls, values):
        if not coord0_less_than_coord1(values["x0"], values["x1"]):
            raise ValueError("x1 must be greater than x0")
        return values

    @root_validator
    def y0_less_than_y1(cls, values):
        if not coord0_less_than_coord1(values["y0"], values["y1"]):
            raise ValueError("y1 must be greater than y0")
        return values


class GroundTruthLabels(BaseModel):
    classification: Optional[str]
    bounding_boxes: Optional[List[BoundingBox]]


class Image(BaseModel):
    id: str
    uri: AnyUrl
    ground_truth_labels: Optional[GroundTruthLabels]

    @validator('uri')
    def check_valid_uri(cls, uri):
        legal_schemes = ['gs', 'http', 'https']
        if uri.scheme not in legal_schemes:
            raise ValueError(
                f'{uri} scheme must be one of {" ".join(legal_schemes)}'
            )

        return uri
