import unittest
from unittest.mock import patch, MagicMock
from app.service.drinkrecordservice import (
    add_drink_record,
    get_drink_record,
    get_drink_record_by_id,
    update_drink_record,
    daily_goal_check
)
from app.model.drinkrecord import DrinkRecord
from azure.cosmos import exceptions

class TestDrinkService(unittest.TestCase):

    @patch('app.db.cosmosconfig.cosmos_db.drink_records_container.create_item')
    def test_add_drink_record(self, mock_create_item):
        # Arrange
        mock_create_item.return_value = None
        record = DrinkRecord(Id="test123", patient_id="patient1", amount_ml=500)

        # Act
        result = add_drink_record(record)

        # Assert
        mock_create_item.assert_called_once_with(body=record.dict(by_alias=True))
        self.assertEqual(result, record)

    @patch('app.db.cosmosconfig.cosmos_db.drink_records_container.query_items')
    def test_get_drink_record(self, mock_query_items):
        # Arrange
        mock_query_items.return_value = [
            {"id": "record1", "patient_id": "patient1", "amount_ml": 300}
        ]

        # Act
        result = get_drink_record("patient1")

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].patient_id, "patient1")
    #
    @patch('app.db.cosmosconfig.cosmos_db.drink_records_container.query_items')
    def test_get_drink_record_by_id(self, mock_query_items):
        # Arrange
        mock_query_items.return_value = [
            {"id": "record1", "patient_id": "patient1", "amount_ml": 300}
        ]

        # Act
        result = get_drink_record_by_id("record1")

        # Assert
        self.assertEqual(result.Id, "record1")
    #

if __name__ == '__main__':
    unittest.main()
