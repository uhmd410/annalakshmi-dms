from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date, datetime

VegStatus = Literal["veg", "non-veg"]
RecordStatus = Literal["active", "inactive"]

class AnnalakshmiBase(BaseModel):
    full_name: str
    mobile_number: str
    email: Optional[str] = None
    address: str
    area: str
    city: str
    state: str
    pin_code: str
    cuisine_specialization: str
    veg_or_nonveg: VegStatus
    signature_dishes: Optional[str] = None
    available_timings: Optional[str] = None
    max_orders_per_day: int = 10
    date_joined: date
    status: RecordStatus = "active"

class AnnalakshmiCreate(AnnalakshmiBase):
    pass

class AnnalakshmiUpdate(BaseModel):
    full_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    area: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None
    cuisine_specialization: Optional[str] = None
    veg_or_nonveg: Optional[VegStatus] = None
    signature_dishes: Optional[str] = None
    available_timings: Optional[str] = None
    max_orders_per_day: Optional[int] = None
    date_joined: Optional[date] = None
    status: Optional[RecordStatus] = None

class AnnalakshmiResponse(AnnalakshmiBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

