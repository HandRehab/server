from pydantic import BaseModel
from typing import Optional

class createUserBody(BaseModel):
    username: str
    name: str
    password: str
    phone: str
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    doctorid: Optional[int] = None
    adminid: Optional[str] = None
    userRole: int
