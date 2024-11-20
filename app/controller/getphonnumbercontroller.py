from fastapi import APIRouter, HTTPException, Depends
from app.service.patientservice import get_patient_id_by_phone_number
from app.authentication.auth import TokenData, require_roles

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.get("/get_patient_id", response_model=dict)
async def get_patient_id(
        current_user: TokenData = Depends(require_roles(["PATIENT", "DRINKAPPUSERS", "CAREGIVERS", "ADMINS"]))
):
    try:
        # Get the phone number from the current user's token
        phone_number = current_user.phone_number
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number not found in the token")

        # Retrieve patient ID using the service method
        patient_id = get_patient_id_by_phone_number(phone_number)

        # Return the patient ID as a response
        return {"patient_id": patient_id}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve patient ID")
