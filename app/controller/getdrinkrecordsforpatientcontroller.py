from fastapi import APIRouter, HTTPException, status, Depends
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import get_drink_record
from typing import List
from app.authentication.auth import TokenData, require_roles
from app.service.patientservice import get_patient_id_by_phone_number
import logging

router = APIRouter(prefix="/api", tags=["Drink Records"])
logger = logging.getLogger("drink_records")

@router.get("/get_patient_records", response_model=List[DrinkRecord])
async def read_drink_record(
        patient_id: str = None,
        current_user: TokenData = Depends(require_roles(["PATIENT", "DRINKAPPUSERS", "CARE_GIVER", "ADMIN"]))
):
    try:
        logger.info(f"Received request for drink records. User roles: {current_user.roles}, Patient ID: {patient_id}")

        # If no patient_id is provided, fetch it using the phone number
        if not patient_id:
            try:
                logger.info(f"Fetching patient_id for phone_number: {current_user.phone_number}")
                patient_id = get_patient_id_by_phone_number(current_user.phone_number)

                if not patient_id:
                    logger.warning(f"Patient ID not found for phone number: {current_user.phone_number}")
                    raise HTTPException(status_code=404, detail="Patient ID not found for the current user")
            except Exception as e:
                logger.error(f"Error while fetching patient_id: {str(e)}")
                raise HTTPException(status_code=500, detail="Error fetching patient ID")

        # Fetch the drink records
        try:
            logger.info(f"Fetching drink records for patient_id: {patient_id}")
            record = get_drink_record(patient_id=patient_id)

            if not record:
                logger.warning(f"No drink records found for patient_id: {patient_id}")
                raise HTTPException(status_code=404, detail="Drink record not found")

            logger.info(f"Drink records retrieved successfully for patient_id: {patient_id}")
            return record

        except Exception as e:
            logger.error(f"Error while fetching drink records: {str(e)}")
            raise HTTPException(status_code=500, detail="Error fetching drink records")

    except HTTPException as http_err:
        # This handles HTTPExceptions explicitly
        logger.warning(f"HTTPException raised: {http_err.detail}")
        raise http_err
    except Exception as e:
        # General exception handler
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
