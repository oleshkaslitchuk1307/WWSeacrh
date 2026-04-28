from pydantic import BaseModel
from pydantic import Field

class MessageCreate(BaseModel):
    receiver_id: int
    message: str = Field(min_length=1, max_length=1000)

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    message: str
    timestamp: str
