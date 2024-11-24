from fastapi import APIRouter, HTTPException, status, Depends
from app.model.drinkrecord import DrinkRecord
from app.service.drinkrecordservice import add_drink_record, get_drink_record
from app.authentication.auth import TokenData, require_roles
from datetime import date
from app.service.patientservice import get_patient_id_by_phone_number

router = APIRouter(prefix="/api", tags=["Drink Records"])

@router.post("/AddRecord", response_model=DrinkRecord, status_code=status.HTTP_201_CREATED)
async def create_drink_record(
    record: DrinkRecord,
    current_user: TokenData = Depends(require_roles(["PATIENT", "CAREGIVERS", "ADMINS"]))
):
    try:
        # Optionally, associate the record with the current user
        record.date = date.today().isoformat()
        record.patient_id = get_patient_id_by_phone_number(current_user.phone_number)  # Assuming `sub` holds the unique identifier for the user

        # Log user interaction for debugging
        print(f"Creating drink record for user: {current_user.phone_number}")

        new_record = add_drink_record(record)
        # Return the serialized dictionary instead of the Pydantic model
        return new_record.dict(by_alias=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
