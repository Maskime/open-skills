from typing import Dict




class RequestUserCreate:

    def __init__(self) -> None:
        super().__init__()
        self.name = ''
        self.first_name = ''
        self.email = ''
        self.password = ''