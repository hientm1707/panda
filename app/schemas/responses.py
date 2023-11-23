from pydantic import BaseModel
from . import BaseResponse

class JobDoc(BaseModel):
    task_id: str

class GenerateCVResponse(BaseResponse):
    docs: list
