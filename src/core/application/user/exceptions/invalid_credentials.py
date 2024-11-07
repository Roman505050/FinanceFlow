class UserInvalidCredentialsException(Exception):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)
