from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from ..database import get_db
from ..rule_generator import generate_rule_json
from app.schemas import CustomerInput
from app.businessrules import evaluate_rules_from_db

router = APIRouter()

@router.post("/scheme", response_model=schemas.Scheme)
def create_scheme_view(scheme: schemas.SchemeCreate, db: Session = Depends(get_db)):
    return crud.create_scheme(db, scheme)

@router.post("/scheme/{scheme_id}/billed-on-cash")
def create_billed_on_cash(scheme_id: str, data: schemas.SchemeBilledOnCashCreate, db: Session = Depends(get_db)):
    return crud.create_billed_on_cash(db, scheme_id, data)

@router.post("/scheme/{scheme_id}/flat-percent")
def create_flat_percent(scheme_id: str, data: schemas.SchemeFlatPercentCreate, db: Session = Depends(get_db)):
    return crud.create_flat_percent(db, scheme_id, data)

@router.post("/scheme/{scheme_id}/free-product")
def create_free_product(scheme_id: str, data: schemas.SchemeFreeProductCreate, db: Session = Depends(get_db)):
    return crud.create_free_product(db, scheme_id, data)

@router.post("/scheme/{scheme_id}/slab")
def create_slab(scheme_id: str, data: schemas.SchemeSlabCreate, db: Session = Depends(get_db)):
    return crud.create_slab(db, scheme_id, data)

@router.post("/scheme/{scheme_id}/applicability")
def add_applicability(scheme_id: str, data: schemas.SchemeApplicabilityBase, db: Session = Depends(get_db)):
    return crud.create_scheme_applicability(db, scheme_id, data)


@router.post("/scheme/{scheme_id}/generate_rule")
def trigger_rule(scheme_id: str, data: schemas.RuleTrigger, db: Session = Depends(get_db)):
    if data.confirm:
        generate_rule_json(scheme_id)
        return {"message": f"Rule generated and stored for scheme {scheme_id}"}
    return {"message": "Rule generation not confirmed"}

@router.post("/evaluate-rules")
def evaluate_rules_api(
    customer: CustomerInput,
    db: Session = Depends(get_db)
):
    result = evaluate_rules_from_db(customer.dict(exclude_none=True), db)
    print(result)
    return {"result": result}