from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class SchemeBase(BaseModel):
    scheme_id: str
    scheme_name: str
    scheme_description: Optional[str] = None
    valid_from: date
    valid_to: date
    customer_category: str
    region: str
    customer_classification: str
    scheme_template: str
    scheme_type: str
    promotion_type: str
    file_url: Optional[str] = None
    is_active: bool
    priority_level: int

class SchemeCreate(SchemeBase):
    pass

class Scheme(SchemeBase):
    created_at: datetime
    class Config:
        orm_mode = True


class SchemeBilledOnCashCreate(BaseModel):
    ptr_based: bool

class SchemeFlatPercentCreate(BaseModel):
    discount_type: str
    discount_value: float
    qualifying_value: int
    operator: str
    basis_type: str

class SchemeFreeProductCreate(BaseModel):
    free_product_code: str
    free_product_name: str
    free_quantity: int
    qualifying_quantity: int

class SchemeSlabCreate(BaseModel):
    from_value: float
    to_value: float
    discount_type: str
    discount_value: float
    slab_basis: str
    operator: str


class SchemeApplicabilityBase(BaseModel):
    criteria: str
    value: str

class RuleTrigger(BaseModel):
    confirm: bool  

class CustomerInput(BaseModel):
    customer_category: Optional[str] = None
    region: Optional[str] = None
    customer_classification: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    purchase_value: Optional[float] = 0
    purchase_quantity: Optional[int] = 0
