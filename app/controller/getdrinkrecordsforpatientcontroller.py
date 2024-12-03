from fastapi import APIRouter, HTTPException, status, Depends
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import get_drink_record
from typing import List
from app.authentication.auth import TokenData, require_roles
from app.service.patientservice import get_patient_id_by_phone_number
import logging

router = APIRouter(prefix="/drinkrecord", tags=["Drink Records"])
logger = logging.getLogger("drink_records")

@router.get("/get_patient_records", response_model=List[DrinkRecord])
async def read_drink_record(
        patient_id: str = None,
        current_user: TokenData = Depends(require_roles(["PATIENT", "DRINKAPPUSERS", "CARE_GIVER", "ADMIN"]))
):
    try:
        if not patient_id:
            try:
                patient_id = get_patient_id_by_phone_number(current_user.phone_number)

                if not patient_id:
                    raise HTTPException(status_code=404, detail="Patient ID not found for the current user")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Error fetching patient ID")

        # Fetch the drink records
        try:
            record = get_drink_record(patient_id=patient_id)

            if not record:
                raise HTTPException(status_code=404, detail="Drink record not found")
            return record

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error fetching drink records")

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
