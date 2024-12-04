from fastapi import APIRouter, HTTPException, Depends

from app.authentication.auth import TokenData, require_roles
from app.service.drinkrecordservice import daily_goal_check
from app.service.patientservice import get_patient_id_by_phone_number

router = APIRouter(prefix="/patient", tags=["Patients"])

@router.get("/daily-goal-check", response_model=str)
async def check_daily_goal(patient_id: str = None, current_user: TokenData = Depends(require_roles(["PATIENT","CARE_GIVER"]))
):
    try:
        if not patient_id:
            patient_id = get_patient_id_by_phone_number(current_user.phone_number)
        result = daily_goal_check(patient_id=patient_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
