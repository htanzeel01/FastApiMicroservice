from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from app.authentication.auth import TokenData, require_roles
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import update_drink_record

router = APIRouter(prefix="/drinkrecord", tags=["Drink Records"])



@router.put("/update-drink-record", response_model=DrinkRecord)
async def edit_drink_record(record_id: str, update_request: DrinkRecord,
        current_user: TokenData = Depends(require_roles(["PATIENT","CARE_GIVER", "ADMIN"]))):
    try:
        updated_record = update_drink_record(record_id=record_id, new_amount_ml=update_request.amount_ml)
        return updated_record
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
