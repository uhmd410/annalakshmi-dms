from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer, ConfigDict
from typing import Optional, Literal
from datetime import date, datetime, timezone
import re

VegStatus = Literal["veg", "non-veg"]
RecordStatus = Literal["active", "inactive"]

MOBILE_PATTERN = r"^[6-9]\d{9}$"   # 10-digit Indian mobile, starts 6-9
PIN_PATTERN = r"^\d{6}$"           # 6-digit Indian PIN code


class AnnalakshmiBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    mobile_number: str
    email: Optional[EmailStr] = None
    address: str = Field(..., min_length=5, max_length=300)
    area: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    pin_code: str
    cuisine_specialization: str = Field(..., min_length=2, max_length=150)
    veg_or_nonveg: VegStatus
    signature_dishes: Optional[str] = Field(None, max_length=500)
    available_timings: Optional[str] = Field(None, max_length=200)
    max_orders_per_day: int = Field(10, gt=0, le=200)
    date_joined: date
    status: RecordStatus = "active"

    @field_validator("full_name", "address", "area", "city", "state", "cuisine_specialization")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("This field cannot be blank")
        return v.strip()

    @field_validator("date_joined")
    @classmethod
    def not_in_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("date_joined cannot be in the future")
        return v
    
    @field_validator("mobile_number")
    @classmethod
    def valid_mobile(cls, v: str) -> str:
        if not re.match(MOBILE_PATTERN, v):
            raise ValueError("Mobile number must be exactly 10 digits and start with 6-9")
        return v

    @field_validator("pin_code")
    @classmethod
    def valid_pin(cls, v: str) -> str:
        if not re.match(PIN_PATTERN, v):
            raise ValueError("PIN code must be exactly 6 digits")
        return v    


class AnnalakshmiCreate(AnnalakshmiBase):
    pass


class AnnalakshmiUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=150)
    mobile_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=5, max_length=300)
    area: Optional[str] = Field(None, min_length=2, max_length=100)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=100)
    pin_code: Optional[str] = None
    cuisine_specialization: Optional[str] = Field(None, min_length=2, max_length=150)
    veg_or_nonveg: Optional[VegStatus] = None
    signature_dishes: Optional[str] = Field(None, max_length=500)
    available_timings: Optional[str] = Field(None, max_length=200)
    max_orders_per_day: Optional[int] = Field(None, gt=0, le=200)
    date_joined: Optional[date] = None
    status: Optional[RecordStatus] = None

    @field_validator("full_name", "address", "area", "city", "state", "cuisine_specialization")
    @classmethod
    def not_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("This field cannot be blank")
        return v.strip() if v else v

    @field_validator("date_joined")
    @classmethod
    def not_in_future(cls, v):
        if v is not None and v > date.today():
            raise ValueError("date_joined cannot be in the future")
        return v

    @field_validator("mobile_number")
    @classmethod
    def valid_mobile(cls, v):
        if v is not None and not re.match(MOBILE_PATTERN, v):
            raise ValueError("Mobile number must be exactly 10 digits and start with 6-9")
        return v

    @field_validator("pin_code")
    @classmethod
    def valid_pin(cls, v):
        if v is not None and not re.match(PIN_PATTERN, v):
            raise ValueError("PIN code must be exactly 6 digits")
        return v


class AnnalakshmiResponse(AnnalakshmiBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "updated_at")
    def serialize_as_utc(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()


class PaginatedAnnalakshmiResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[AnnalakshmiResponse]