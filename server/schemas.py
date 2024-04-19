from pydantic import BaseModel

class Load(BaseModel):
    query: str
    
class Pdf(BaseModel):
    query: str
    output: str