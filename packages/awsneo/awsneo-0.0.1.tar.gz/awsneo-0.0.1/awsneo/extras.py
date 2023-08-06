from enum import Enum


class ConnectionException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'There was an error trying to connecting to database, {0} '.format(self.message)


class QueryingException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'There was an error executing query, {0} '.format(self.message)


class NoSuchConnectionException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'You must provide at least one parameter. Bucket and file or just the query through the parameters, {0}'\
            .format(self.message)


class SecretManagerException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'There was an error retrieving the data located in secret, {0} '.format(
            self.message)


class BucketReadFileException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'There was an error getting the object from bucket, {0} '.format(self.message)


class Results(Enum):
    JSON = 1
    DICT = 2
    DF = 3
