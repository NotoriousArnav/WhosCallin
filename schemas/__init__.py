from .Survey import SurveyData 
from .PassthroughData import PassthroughData
from .Phones import Phone
from .Addresses import Address
from pydantic import BaseModel, Field
from typing import List, Optional

class CallerInfo(BaseModel):
    id: str
    name: str
    score: float
    access: str
    enhanced: bool
    phones: List[Phone]
    addresses: List[Address]
    internetAddresses: list = Field(default_factory=list)
    badges: list = Field(default_factory=list)
    tags: list = Field(default_factory=list)
    cacheTtl: int
    sources: list = Field(default_factory=list)
    searchWarnings: list = Field(default_factory=list)
    surveys: List[SurveyData]
    commentsStats: dict
    manualCallerIdPrompt: bool
    ns: int

    @classmethod
    def from_dict(cls, data: dict) -> "CallerInfo":
        """
        Create a CallerInfo instance from a dictionary.
        Build a CallerInfo instance from a dictionary representation of the data but manually
        """
        
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            score=data.get("score", 0.0),
            access=data.get("access", ""),
            enhanced=data.get("enhanced", False),
            phones=[Phone.from_dict(phone) for phone in data.get("phones", [])],
            addresses=[Address.from_dict(address) for address in data.get("addresses", [])],
            internetAddresses=data.get("internetAddresses", []),
            badges=data.get("badges", []),
            tags=data.get("tags", []),
            cacheTtl=data.get("cacheTtl", 0),
            sources=data.get("sources", []),
            searchWarnings=data.get("searchWarnings", []),
            surveys=[SurveyData.from_dict(survey) for survey in data.get("surveys", [])],
            commentsStats=data.get("commentsStats", {}),
            manualCallerIdPrompt=data.get("manualCallerIdPrompt", False),
            ns=data.get("ns", 0)
        )
