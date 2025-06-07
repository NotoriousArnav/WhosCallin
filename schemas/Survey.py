"""
# Schema for Survey Data
"""
from pydantic import BaseModel
from .PassthroughData import PassthroughData

class SurveyData(BaseModel):
    id: str
    frequency: int
    passthrough: PassthroughData
    pernNumberCooldown: int
    dynamicContentAccessKey: str

    @classmethod
    def from_dict(cls, data: dict) -> "SurveyData":
        """
        Create a SurveyData instance from a dictionary.
        """
        passthrough_data = PassthroughData.from_base64(data.get("passthroughData", ""))
        return cls(
            id=data.get("id", ""),
            frequency=data.get("frequency", 0),
            passthrough=passthrough_data,
            pernNumberCooldown=data.get("perNumberCooldown", 0),
            dynamicContentAccessKey=data.get("dynamicContentAccessKey", "")
        )
