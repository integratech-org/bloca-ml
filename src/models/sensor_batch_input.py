from pydantic import BaseModel, ConfigDict, Field


class SensorBatchInput(BaseModel):
    compaction_temp_c: float = Field(
        ...,
        ge=100.0,
        le=200.0,
        description="Mean of last 10 readings (~10s) at peak heating phase. Sensor: K-type thermocouple.",
    )

    hydraulic_pressure_mpa: float = Field(
        ...,
        ge=0.0,
        le=25.0,
        description=(
            "Max value observed during the compression phase. Sensor: inline hydraulic "
            "pressure transducer on the jack's hydraulic line (0-20/25 MPa, 4-20mA or "
            "0-5V output). Replaces the 50kg load cell originally specified -- the load "
            "cell under-reads the multi-ton force a hydraulic jack applies to a mold "
            "this size, so it cannot give an accurate compaction-pressure reading. "
            "Operating hold-pressure at the mold face is ~0.14 MPa (20 psi); initial "
            "compaction pressure before the plastic softens runs higher."
        ),
    )

    heating_duration_min: float = Field(
        ...,
        ge=0.0,
        le=60.0,
        description="Elapsed time from start of heating to start of compression. Source: RTC timestamp delta.",
    )

    cooling_duration_min: float = Field(
        ...,
        ge=0.0,
        le=60.0,
        description="Elapsed time from end of compression to sensor readout. Source: RTC timestamp delta.",
    )

    compressed_height_mm: float = Field(
        ...,
        ge=30.0,
        le=80.0,
        description="Mean of last 10 readings after compression settles. Sensor: ultrasonic distance sensor.",
    )

    heater_current_a: float = Field(
        ...,
        ge=0.0,
        le=20.0,
        description="Mean current over the full heating_duration_min window. Sensor: ACS712 (20A variant assumed).",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": {
                "compaction_temp_c": 152.4,
                "compression_load_kgf": 480.0,
                "heating_duration_min": 18.5,
                "cooling_duration_min": 12.0,
                "compressed_height_mm": 55.2,
                "heater_current_a": 4.1,
            }
        }
    )
