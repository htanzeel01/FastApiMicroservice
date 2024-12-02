from fastapi import APIRouter, HTTPException, Depends

from app.authentication.auth import TokenData, require_roles
from app.service.drinkrecordservice import daily_goal_check

router = APIRouter(prefix="/api", tags=["Patients"])

@router.get("/daily_goal_check", response_model=str)
async def check_daily_goal(patient_id: str = None, current_user: TokenData = Depends(require_roles(["PATIENT","CARE_GIVER"]))
):
    try:
        result = daily_goal_check(patient_id=patient_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
