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
