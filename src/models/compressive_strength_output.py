from pydantic import BaseModel, ConfigDict, Field


class CompressiveStrengthOutput(BaseModel):
    compressive_strength_mpa: float = Field(
        ...,
        ge=0.0,
        le=15.0,
        description="Predicted compressive strength in MPa, from the Random Forest regression model. Target operating band: 3-8 MPa.",
    )

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"compressive_strength_mpa": 6.3}]}
    )
