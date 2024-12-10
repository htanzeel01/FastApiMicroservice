from fastapi import APIRouter, HTTPException, Depends
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import get_drink_record
from app.service.patientservice import get_patient_id_by_phone_number
from app.authentication.auth import TokenData, require_roles
from typing import List

router = APIRouter(prefix="/drinkrecords", tags=["DrinkRecords"])

@router.get("/patient", response_model=List[DrinkRecord], summary="Retrieve patient drink records")
async def read_drink_record(
    patient_id: str = None,
    current_user: TokenData = Depends(require_roles(["PATIENT", "DRINKAPPUSERS", "CARE_GIVER", "ADMIN"]))
):
    try:
        # If patient_id is not provided, fetch it using the current user's phone number
        if not patient_id:
            patient_id = get_patient_id_by_phone_number(current_user.phone_number)
            if not patient_id:
                raise HTTPException(status_code=404, detail="Patient ID not found for the current user")

        # Fetch the drink records for the provided patient_id
        records = get_drink_record(patient_id=patient_id)
        if not records:
            raise HTTPException(status_code=404, detail="Drink records not found")

        return records

    except HTTPException as http_err:
        raise http_err  # Re-raise HTTP-specific exceptions without modification

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
