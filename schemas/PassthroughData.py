"""
# Schema for Passthrough Data
"""
from pydantic import BaseModel
from typing import Optional
import base64
import simdjson

class PassthroughData(BaseModel):
    phone: Optional[str]
    name: Optional[str]
    uuid: Optional[str]
    # Additional fields that I could not understand but they exist in the data
    field_22: Optional[str]
    field_21: Optional[str]
    field_4: Optional[str]
    field_8: Optional[str]
    field_5: Optional[str]

    @classmethod
    def from_base64(cls, b64_string: str) -> "PassthroughData":
        decoded_bytes = base64.b64decode(b64_string)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Parser
        parser = simdjson.Parser()

        json_data = parser.parse(decoded_str)

        mapped_data = {
            "field_22": json_data.get("22", None),
            "field_21": json_data.get("21", None),
            "field_4": json_data.get("4", None),
            "field_8": json_data.get("8", None),
            "phone": json_data.get("3", None),
            "name": json_data.get("2", None),
            "uuid": json_data.get("23", None),
            "field_5": json_data.get("5", None),
        }

        return cls(**mapped_data)
