from pydantic import BaseModel

# Define the Patient model class
class Patient(BaseModel):
    Id: str              # ID field (integer)
    daily_goal: float     # Daily goal (float for more precision)


