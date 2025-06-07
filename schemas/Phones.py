"""
# Schema for Phone Data
"""
from pydantic import BaseModel


class Phone(BaseModel):
    e164Format: str
    numberType: str
    nationalFormat: str
    dialingCode: int
    countryCode: str
    carrier: str
    type: str

    @classmethod
    def from_dict(cls, data: dict) -> "Phone":
        return cls(
            e164Format=data.get("e164Format", ""),
            numberType=data.get("numberType", ""),
            nationalFormat=data.get("nationalFormat", ""),
            dialingCode=data.get("dialingCode", 0),
            countryCode=data.get("countryCode", ""),
            carrier=data.get("carrier", ""),
            type=data.get("type", "")
        )

