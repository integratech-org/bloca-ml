from pydantic import BaseModel, ConfigDict, Field


class QualityClassOutput(BaseModel):
    quality_class: int = Field(
        ...,
        ge=0,
        le=2,
        description="Predicted surface-quality class from the CNN classifier: 0 = Acceptable, 1 = Defective, 2 = Reject.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Softmax confidence score for the predicted class, from 0 to 1.",
    )

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"quality_class": 0, "confidence": 0.94}]}
    )
