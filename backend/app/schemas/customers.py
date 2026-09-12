from pydantic import BaseModel


class CustomerListItem(BaseModel):
    id: int
    name: str
    phone: str
    current_plan: str
    service_type: str | None = None
    segment: str | None = None