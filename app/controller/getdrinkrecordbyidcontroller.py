from fastapi import APIRouter, Depends, HTTPException, status
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import get_drink_record_by_id
from app.authentication.auth import require_roles, TokenData

router = APIRouter(prefix="/api", tags=["Drink Records"])

@router.get("/byid", response_model=DrinkRecord, summary="Get Drink Record by ID")
async def read_drink_record_by_id(id: str = None,current_user: TokenData = Depends(require_roles(["ADMINS"]))
):

    # Authentication and role checks are enforced by dependencies
    try:
        record = get_drink_record_by_id(id=id)
        return record
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
