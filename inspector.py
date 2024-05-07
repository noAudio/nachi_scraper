from dataclasses import dataclass


@dataclass
class Inspector:
    name: str
    phone: str
    company: str
    serviceArea: str
    profileLink: str
    website: str = 'n/a'

    def __init__(self, name: str, phone: str, company: str, serviceArea: str, profileLink: str) -> None:
        self.name = name
        self.phone = phone
        self.company = company
        self.serviceArea = serviceArea
        self.profileLink = profileLink
