from pydantic import BaseModel, Field


class HealthcheckResponseSchema(BaseModel):
    status: str = Field(json_schema_extra={"example": "ok"})
