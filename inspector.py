class Inspector:
    name: str
    phone: str
    website: str

    def __init__(self, name: str, phone: str, website: str = '') -> None:
        self.name = name
        self.phone = phone
        self.website = website
