from .base import OurBaseModel

class TokenResponse(OurBaseModel):
    access_token: str
    expires_in: int