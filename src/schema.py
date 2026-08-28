from typing import Optional
from pydantic import BaseModel, HttpUrl


class BookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_gbp: float
    price_text: str
    availability_text: str
    rating_text: Optional[str] = None
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str