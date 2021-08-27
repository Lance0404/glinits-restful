# Common Exception that may be raise from the API call
class Common(Exception):
    """Exception raised for common types.

    find more examples here:
    https://www.programiz.com/python-programming/user-defined-exception
    """

    def __init__(self, message="error of common type"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'customized message for print here: {self.message}'
