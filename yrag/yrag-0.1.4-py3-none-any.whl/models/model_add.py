from pydantic import BaseModel
from  .config import z

class data(BaseModel):
    x:int
    y:int
def model_add(data:data):
    return data.x + data.y