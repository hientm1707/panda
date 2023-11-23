from . import BaseRequest

class GenerateCVRequest(BaseRequest):
    cv: str
    jds: list[str] = []
