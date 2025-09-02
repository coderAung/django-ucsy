from dataclasses import dataclass
from typing import Optional
from django.core.files.uploadedfile import InMemoryUploadedFile
@dataclass
class AccountDetailDTO:
    name: str = ''
    phone: str = ''
    address: str = ''
    profile_image: Optional[InMemoryUploadedFile] = None

def account_staff_dto(**kwargs) -> AccountDetailDTO:
    return AccountDetailDTO(**kwargs)