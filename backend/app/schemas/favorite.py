from pydantic import BaseModel
from app.models.favorite import FavoriteType

class FavoriteEntryCreate(BaseModel):
    item_type: FavoriteType 
    item_id: int 

class FavoriteEntryOut(BaseModel):
    id: int 
    item_type: FavoriteType 
    item_id: int 

    model_config = {"from_attributes": True}

