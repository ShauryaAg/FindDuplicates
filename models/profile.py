import re
from datetime import date
from typing import Optional
from pydantic import BaseModel, constr, conint, validator


class Profile(BaseModel):
    first_name: str
    last_name: str
    class_year: conint(gt=0)
    date_of_birth: Optional[date]
    email_field: constr(regex="^[\w\.\-\+]+@([\w-]+\.)+[\w-]{2,4}$")

    @validator('email_field', pre=True, always=True)
    def validate_email(cls, email):
        """ 
        Substituting every after `+` with '' as most email providers ignore that part
        """
        return re.sub(r'(\+.*(?=@))', '', email)
