from fastapi import APIRouter, HTTPException, status, Depends
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import add_drink_record
from app.authentication.auth import TokenData, require_roles
from datetime import date
from app.service.patientservice import get_patient_id_by_phone_number

router = APIRouter(prefix="/drinkrecord", tags=["DrinkRecords"])


# Controller for the caregiver to input patient drink record
@router.post("/newrecordbycaregiver", response_model=DrinkRecord, status_code=status.HTTP_201_CREATED)
async def create_drink_record_caregiver(
        record: DrinkRecord,
        patient_phone_number: str,  # Accept phone number as a query parameter
        current_user: TokenData = Depends(require_roles(["CARE_GIVER", "ADMIN"]))
):
    try:
        # Fetch patient_id using patient_phone_number
        patient_id = get_patient_id_by_phone_number(patient_phone_number)

        # Optionally associate the record with the current user
        record.date = date.today().isoformat()
        record.patient_id = patient_id  # Assign the fetched patient_id

        # Add the new drink record to the database
        new_record = add_drink_record(record)

        # Return the serialized dictionary instead of the Pydantic model
        return new_record.dict(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
