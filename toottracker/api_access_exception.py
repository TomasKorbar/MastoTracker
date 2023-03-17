class ApiAccessException(Exception):
    """ Exception indicating that error has been encountered while accessing API"""

    def __init__(self, status_code: int, message: str, api_error: str | None = None):
        """

        Parameters
        ----------
        status_code : int
            Http status code of response

        message : str
            Context of exception

        api_error : str
             (Default value = None)
            Error description from response body if provided

        Returns
        -------

        """
        super(message)
        self.status_code = status_code
        self.api_error = api_error
