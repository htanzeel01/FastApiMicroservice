from fastapi import APIRouter, HTTPException, status, Depends
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import get_drink_record
from typing import List
from app.authentication.auth import TokenData, require_roles
from app.service.patientservice import get_patient_id_by_phone_number

router = APIRouter(prefix="/api", tags=["Drink Records"])


@router.get("/get_patient_records", response_model=List[DrinkRecord])
async def read_drink_record(
        patient_id: str = None,  # Make patient_id optional
        current_user: TokenData = Depends(require_roles(["PATIENT", "DRINKAPPUSERS", "CAREGIVERS", "ADMINS"]))
):
    try:
        # If patient_id is not provided, use the phone number from the authenticated user to get the patient_id
        if not patient_id:
            patient_id = get_patient_id_by_phone_number(current_user.phone_number)

        # Fetch the drink records using the patient_id
        record = get_drink_record(patient_id=patient_id)  # Pass the patient_id here
        if not record:
            raise HTTPException(status_code=404, detail="Drink record not found")

        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
