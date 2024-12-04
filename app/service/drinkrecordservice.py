import uuid

from app.db.cosmosconfig import cosmos_db
from app.model.drinkrecord import DrinkRecord
from azure.cosmos import exceptions
from typing import List
from app.service.patientservice import get_daily_goal_by_id
from datetime import date

def add_drink_record(record: DrinkRecord) -> DrinkRecord:
    try:
        print(record)
        #record.Id = uuid.UUID

        cosmos_db.drink_records_container.create_item(body=record.dict(by_alias=True))
        return record
    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to add drink record: {e}")
        raise e


def get_drink_record(patient_id: str) -> List[DrinkRecord]:
    try:
        query = "SELECT * FROM c WHERE c.patient_id=@patient_id"
        parameters = [
            {"name": "@patient_id", "value": patient_id}
        ]
        items = list(cosmos_db.drink_records_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        if not items:
            return []
        return [DrinkRecord(**item) for item in items]
    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to retrieve drink record: {e}")
        raise e
def get_drink_record_by_id(id: str) -> DrinkRecord:
    try:
        query = "SELECT * FROM c WHERE c.id=@Id"
        parameters = [
            {"name": "@Id", "value": id}
        ]
        items = list(cosmos_db.drink_records_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        if not items:
            raise ValueError("Drink record not found")
        return DrinkRecord(**items[0])
    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to retrieve drink record: {e}")
        raise e


def update_drink_record(record_id: str, new_amount_ml: float) -> DrinkRecord:
    try:
        query = "SELECT * FROM c WHERE c.id=@record_id"
        parameters = [
            {"name": "@record_id", "value": record_id}
        ]
        items = list(cosmos_db.drink_records_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        print(f"Query result: {items}")  # Debug print statement
        if not items:
            raise ValueError("Drink record not found")

        item = items[0]
        item['amount_ml'] = new_amount_ml

        cosmos_db.drink_records_container.replace_item(item=item['id'], body=item)

        return DrinkRecord(**item)
    except exceptions.CosmosHttpResponseError as e:
        print(f"Failed to update drink record: {e}")
        raise e


def daily_goal_check(patient_id: str) -> str:
    try:
        # Get drink records
        drink_records = get_drink_record(patient_id)
        # Filter records for today
        today = date.today()
        today_records = [record for record in drink_records if record.date == today]
        #print(f"Drink records for patient {patient_id} today: {today_records}")  # Debug statement

        # Get daily goal
        daily_goal = get_daily_goal_by_id(patient_id)
        #print(f"Daily goal for patient {patient_id}: {daily_goal}")  # Debug statement

        # Calculate total amount drunk today
        total_amount = sum(record.amount_ml for record in today_records)
        #print(f"Total amount drunk by patient {patient_id} today: {total_amount}")  # Debug statement

        # Compare with daily goal
        if total_amount >= daily_goal:
            return "Goal has been reached. No need to drink more."
        else:
            remaining = daily_goal - total_amount
            return f"{remaining} ml left to reach the daily goal."
    except ValueError as e:
        return str(e)
    except exceptions.CosmosHttpResponseError as e:
        return f"Failed to perform daily goal check: {e}"
