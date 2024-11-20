from app.db.cosmosconfig import cosmos_db
from app.model.patient import Patient
from azure.cosmos import exceptions


def get_daily_goal_by_id(patient_id: str) -> float:
    try:
        query = "SELECT c.DailyGoal FROM c WHERE c.Id=@patient_id"
        parameters = [
            {"name": "@patient_id", "value": patient_id}
        ]

        items = list(cosmos_db.patients_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        if not items:
            raise ValueError("Patient not found")

        print(f"Patient's daily goal: {items[0]['DailyGoal']}")  # Debug statement
        return items[0]['DailyGoal']

    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to retrieve patient's daily goal: {e}")
        raise e
# Method to update the daily goal by patient ID
def update_daily_goal_by_id(patient_id: str, new_goal: float) -> None:
    try:
        # Query to find the patient document by ID
        query = "SELECT * FROM c WHERE c.Id=@patient_id"
        parameters = [
            {"name": "@patient_id", "value": patient_id}
        ]

        items = list(cosmos_db.patients_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        if not items:
            raise ValueError("Patient not found")

        patient_doc = items[0]
        patient_doc['DailyGoal'] = new_goal  # Update the daily goal field

        # Replace the document with the updated content
        cosmos_db.patients_container.replace_item(
            item=patient_doc['id'],
            body=patient_doc
        )

        print(f"Updated patient's daily goal to: {new_goal}")  # Debug statement

    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to update patient's daily goal: {e}")
        raise e

# Method to get the patient ID by phone number
def get_patient_id_by_phone_number(phone_number: str) -> str:
    try:
        # Query to find the patient document by phone number
        query = "SELECT c.Id FROM c WHERE c.PhoneNumber=@phone_number"
        parameters = [
            {"name": "@phone_number", "value": phone_number}
        ]

        items = list(cosmos_db.patients_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        if not items:
            raise ValueError("Patient with the provided phone number not found")

        print(f"Retrieved patient ID: {items[0]['Id']}")  # Debug statement
        return items[0]['Id']

    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to retrieve patient ID by phone number: {e}")
        raise e



