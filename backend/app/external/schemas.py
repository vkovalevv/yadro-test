from pydantic import BaseModel, Field


class ExternalUser(BaseModel):
    first_name: str = Field(alias='FirstName')
    last_name: str = Field(alias='LastName')
    gender: str = Field(alias='Gender')
    phone: str = Field(alias='Phone')
    email: str = Field(alias='Email')
    address: str = Field(alias='Address')
    
