from pydantic import BaseModel

class SentenceInput(BaseModel):
    session_id : str
    sentence : str = ""

class RoomIdInput(BaseModel):
    session_id : str