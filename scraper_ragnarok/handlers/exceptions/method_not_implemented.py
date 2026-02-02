class MethodNotImplemented(BaseException):
    def __init__(self, message="Method not implemented"):
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"
