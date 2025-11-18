from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class Contact(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    company: Optional[str] = None
    message: str = Field(..., min_length=5, max_length=5000)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
