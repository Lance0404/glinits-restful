"""
[ref](https://stackoverflow.com/a/1319675)
"""

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

class InvalidUrlPath(Exception):
    message = "Invalid URL path: "
    def __init__(self, action: str):
        self.message += action
        super().__init__(self.message)

    def __str__(self):
        return f'<InvalidUrlPath: {self.message}>'

class CommitError(Exception):
    pass

class DishNotInRestaurant(Exception):
    pass

class UserNoMoney(Exception):
    pass

class UserNotFound(Exception):
    pass