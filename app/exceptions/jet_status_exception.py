class JetIQStatusCodeError(Exception):
    """Exception if JetIQ status code is not 200"""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
