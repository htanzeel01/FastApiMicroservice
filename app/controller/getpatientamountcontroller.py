from fastapi import APIRouter, HTTPException, status, Depends

from app.authentication.auth import TokenData, require_roles
from app.service.patientservice import get_daily_goal_by_id, get_patient_id_by_phone_number

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.get("/get_daily_goal_by_id", response_model=float)
async def read_daily_goal(
        patient_id: str = None,  # Make patient_id optional
        current_user: TokenData = Depends(require_roles(["PATIENT","CAREGIVERS", "ADMINS"]))
):
    try:
        if not patient_id:
            patient_id = get_patient_id_by_phone_number(current_user.phone_number)
        daily_goal = get_daily_goal_by_id(patient_id=patient_id)
        return daily_goal
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
