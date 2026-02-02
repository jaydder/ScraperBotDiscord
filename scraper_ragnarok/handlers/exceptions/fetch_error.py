class FetchError(BaseException):
    def __init__(self, url, message='error accessing URL'):
        self.url = url
        super().__init__(message)

    def __str__(self):
        return f'{self.url} -> {self.message}'
