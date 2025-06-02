from sqlalchemy import Column, String, Text, Date, Enum, Boolean, Integer, ForeignKey, UUID, DECIMAL, TIMESTAMP,DateTime,JSON
import uuid
from app.database import Base

class Scheme(Base):
    __tablename__ = "scheme"

    scheme_id = Column(String, primary_key=True, index=True)
    scheme_name = Column(String)
    scheme_description = Column(Text)
    valid_from = Column(Date)
    valid_to = Column(Date)
    customer_category = Column(String)
    region = Column(String)
    customer_classification = Column(String)
    scheme_template = Column(String)
    scheme_type = Column(String)
    promotion_type = Column(String)
    file_url = Column(String)
    is_active = Column(Boolean)
    priority_level = Column(Integer)
    created_at = Column(TIMESTAMP)

class SchemeBilledOnCash(Base):
    __tablename__ = "scheme_billed_on_cash"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_id = Column(String, ForeignKey("scheme.scheme_id"))
    ptr_based = Column(Boolean)

class SchemeFlatPercent(Base):
    __tablename__ = "scheme_flat_percent"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_id = Column(String, ForeignKey("scheme.scheme_id"))
    discount_type = Column(String)
    discount_value = Column(DECIMAL)
    qualifying_value = Column(Integer)
    operator = Column(String)
    basis_type = Column(String)

class SchemeFreeProduct(Base):
    __tablename__ = "scheme_free_product"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_id = Column(String, ForeignKey("scheme.scheme_id"))
    free_product_code = Column(String)
    free_product_name = Column(String)
    free_quantity = Column(Integer)
    qualifying_quantity = Column(Integer)

class SchemeSlab(Base):
    __tablename__ = "scheme_slab"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_id = Column(String, ForeignKey("scheme.scheme_id"))
    from_value = Column(DECIMAL)
    to_value = Column(DECIMAL)
    discount_type = Column(String)
    discount_value = Column(DECIMAL)
    slab_basis = Column(String)
    operator = Column(String)


class SchemeApplicability(Base):
    __tablename__ = "scheme_applicability"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_id = Column(String, ForeignKey("scheme.scheme_id"))
    criteria = Column(String)
    value = Column(String)

class SchemeRuleJson(Base):
    __tablename__ = "scheme_rule_json"  # use correct table name

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scheme_id = Column(String)
    rule_json = Column(JSON)  # use JSON if using SQLite, JSONB if PostgreSQL
    generated_at = Column(DateTime)