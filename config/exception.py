class BaseDomainException(Exception):
    message = 'An error occurred'
    status_code = 500

    def __init__(
        self, message: str | None = None, status_code: int | None = None
    ):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)
