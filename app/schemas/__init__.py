from pydantic import BaseModel, ConfigDict

class BaseRequest(BaseModel):
    pass

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)