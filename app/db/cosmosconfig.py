from azure.cosmos import CosmosClient, PartitionKey, exceptions
from app.config import config

class CosmosDB:
    def __init__(self):
        try:
            # Initialize Cosmos DB client
            self.client = CosmosClient(config.DBURI, credential=config.dbkey)

            # Get database client
            self.database = self.client.get_database_client(config.DBName)

            # Create DrinkRecords container if not exists
            self.drink_records_container = self.database.create_container_if_not_exists(
                id='DrinkRecords',
                partition_key=PartitionKey(path="/Id"),  # Partition key for DrinkRecords
                offer_throughput=400
            )

            # Create Patients container if not exists
            self.patients_container = self.database.create_container_if_not_exists(
                id='Patients',
                partition_key=PartitionKey(path="/Id"),  # Assuming 'id' is used as partition key for Patient
                offer_throughput=400
            )

        except exceptions.CosmosHttpResponseError as e:
            print(f"Cosmos DB connection failed: {e}")
            raise e

# Singleton instance for accessing Cosmos DB
cosmos_db = CosmosDB()
