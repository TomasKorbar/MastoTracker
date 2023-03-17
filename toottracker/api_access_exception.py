class ApiAccessException(Exception):
    def __init__(self, status_code, message, api_error = None):
        super(message)
        self.status_code = status_code
        self.api_error = api_error