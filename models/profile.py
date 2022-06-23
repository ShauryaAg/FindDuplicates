from datetime import date
from typing import Optional
from pydantic import BaseModel, constr, conint


class Profile(BaseModel):
    first_name: str
    last_name: str
    class_year: conint(gt=0)
    date_of_birth: Optional[date]
    email_field: constr(regex="^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$")
