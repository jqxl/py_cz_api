class TokenExpiredError(Exception):
    """Exception raised when a JWT token has expired."""
    def __init__(self, message:str ="JWT token is expired."):
        self.message = message
        super().__init__(self.message)