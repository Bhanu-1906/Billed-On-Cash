from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
import json

def create_scheme(db: Session, scheme: schemas.SchemeCreate):
    db_scheme = models.Scheme(**scheme.dict(), created_at=datetime.utcnow())
    db.add(db_scheme)
    db.commit()
    db.refresh(db_scheme)
    return db_scheme

def create_billed_on_cash(db: Session, scheme_id: str, data: schemas.SchemeBilledOnCashCreate):
    entry = models.SchemeBilledOnCash(scheme_id=scheme_id, **data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def create_flat_percent(db: Session, scheme_id: str, data: schemas.SchemeFlatPercentCreate):
    entry = models.SchemeFlatPercent(scheme_id=scheme_id, **data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def create_free_product(db: Session, scheme_id: str, data: schemas.SchemeFreeProductCreate):
    entry = models.SchemeFreeProduct(scheme_id=scheme_id, **data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def create_slab(db: Session, scheme_id: str, data: schemas.SchemeSlabCreate):
    entry = models.SchemeSlab(scheme_id=scheme_id, **data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def create_scheme_applicability(db: Session, scheme_id: str, data: schemas.SchemeApplicabilityBase):
    new_row = models.SchemeApplicability(scheme_id=scheme_id, **data.dict())
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row


def store_rule_json(db: Session, scheme_id: str, rule_data: dict):
    rule_entry = models.RuleJSON(
        scheme_id=scheme_id,
        rule=json.dumps(rule_data, indent=2)
    )
    db.add(rule_entry)
    db.commit()
    db.refresh(rule_entry)
    return rule_entry