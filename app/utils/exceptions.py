from fastapi import HTTPException
from psycopg2 import OperationalError


class DeployError(Exception):
    """
    Exception Handler for Deployment Error
    """

    def __init__(self, error):
        self.error = error

    @staticmethod
    def db_starting_up(ex: OperationalError) -> bool:
        """
        Checks problems when DB server is start up
        Return True/False
        """
        failure = False
        if str(ex).find("the database system is starting up") > 0:
            failure = True
        return failure


class InvalidAccount(Exception):
    """Account not found exception"""

    pass


class InMemoryManagerConnectionError(Exception):
    """In memory instance connection error"""

    pass


class AuthError(HTTPException):
    """Exception Handler for Auth Error"""

    def __init__(self, error, status_code):
        self.detail = error
        self.status_code = status_code
