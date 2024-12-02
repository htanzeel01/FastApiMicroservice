from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from app.controller.adddrinkrecordcontroller import router as add_drinks
from app.controller.getdrinkrecordsforpatientcontroller import router as get_patients_records
from app.controller.updatedrinkrecordcontroller import router as update_records
from app.controller.getdrinkrecordbyidcontroller import router as getbyid
from app.controller.dailygoalcheckcontroller import router as dailygoal
from app.controller.updatedailygoalcontroller import router as update_dailygoal
from app.controller.adddrinkrecordcaregiver import router as add_record_caregiver

def create_app() -> FastAPI:
    app = FastAPI(
        title="Drink Record Service",
        description="API for recording drink intake for elderly patients.",
        version="1.0.0",
        openapi_tags=[
            {
                "name": "Drink Records",
                "description": "Operations with drink records."
            }
            # Add more tags if necessary
        ]
    )

    # Add CORS middleware if needed
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this to your frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(add_drinks)
    app.include_router(get_patients_records)
    app.include_router(update_records)
    app.include_router(getbyid)
    app.include_router(dailygoal)
    app.include_router(update_dailygoal)
    app.include_router(add_record_caregiver)

    # Customize OpenAPI schema to include security schemes
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        # Define the security scheme
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
        # Apply the security scheme globally
        openapi_schema["security"] = [
            {"BearerAuth": []}
        ]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app
