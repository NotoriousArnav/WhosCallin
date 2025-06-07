"""
# Schema for Addresses Data
"""
from pydantic import BaseModel
from typing import Optional, List

class InternetAddress(BaseModel):
    id: str
    service: str
    caption: str
    type: str

class Address(BaseModel):
    """
    Example Address Data
    ```json
    {
      "city": "West Bengal",
      "countryCode": "IN",
      "timeZone": "+05:30",
      "type": "address"
      ...
    }
    ```
    """
    city: Optional[str] = None
    countryCode: Optional[str] = None
    timeZone: Optional[str] = None
    type: Optional[str] = None
    # Add other fields as necessary

    @classmethod
    def from_dict(cls, data: dict) -> "Address":
        """
        Create an Address instance from a dictionary.
        """
        return cls(
            city=data.get("city"),
            countryCode=data.get("countryCode"),
            timeZone=data.get("timeZone"),
            type=data.get("type"),
            # Add other fields as necessary
        )
