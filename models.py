from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str  # Will store hashed password

class EmergencyService(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str = "Pending"  # Can be Pending, In Progress, Resolved
    latitude: float
    longitude: float
    priority: int = Field(default=1)  # 1 (Low), 2 (Medium), 3 (High)
    user_id: int  # FK to User
