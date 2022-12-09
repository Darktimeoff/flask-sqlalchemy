
class NotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ValidationDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)