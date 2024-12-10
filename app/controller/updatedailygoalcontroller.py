from fastapi import APIRouter, HTTPException, Depends
from app.service.patientservice import update_daily_goal_by_id, get_patient_id_by_phone_number
from app.model.patient import Patient
from app.authentication.auth import require_roles  # Ensure this is imported from your auth module
from app.authentication.auth import TokenData  # Import the TokenData class

router = APIRouter(prefix="/patient", tags=["Patients"])


# Define a model for request body validation


@router.put("/dailygoal", response_model=None)
async def update_patient_daily_goal(
        request: Patient,
        current_user: TokenData = Depends(require_roles(["PATIENT", "CARE_GIVER", "ADMIN"]))
):
    try:
        # Get the phone number from the current user
        phone_number = current_user.phone_number
        # Example: Use phone_number to get patient ID
        patient_id = get_patient_id_by_phone_number(phone_number)
        # Call the service method to update the daily goal
        update_daily_goal_by_id(patient_id,request.daily_goal)
        return {"message": "Daily goal updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update daily goal")
