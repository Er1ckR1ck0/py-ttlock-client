from pydantic import BaseModel, ConfigDict


class TTLockSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class BaseLockCreate(TTLockSchema):
    clientId: str
    accessToken: str
    date: int
