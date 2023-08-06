from contextlib import suppress
from dataclasses import dataclass
from re import search
from json import loads

import pandas as pd

from .extras import ConnectionException, NoSuchConnectionException, QueryingException, Results
from .utils import get_connection_data, get_script_content


@dataclass
class DBConnector:
    """
        Create a connection instance to execute queries

        :type secret_id: string
        :param secret_id: Arn from the secret manager
            You must first make sure that you have the permissions on the resource to invoke

        :type dict_connection: string
        :param dict_connection: Dictionary with connection values (host, username, password, database, driver, port)

        :type timeout: int
        :param timeout: Timeout

        :raises:
            ConnectionException: If provided data through direct connection or secret value are wrong to establish connection
            NotImplementedError: If the driver property has an unmapped value ({PostgreSQL}, {MySQL}, {SQL Server #})
    """

    def __init__(self, secret_id: str = None, dict_connection: dict = None, timeout: int = 5):

        condition = secret_id is not None

        condition2 = dict_connection is not None

        if condition and condition2:
            raise Exception(
                "You can only send one argument 'secret_id' or 'dict_connection', and two were received")
        elif condition or condition2:
            if condition:
                _data = get_connection_data(secret_id)
                if isinstance(_data, str):
                    _data = loads(_data)
            else:
                _data = dict_connection
        else:
            raise ValueError(
                "'secret_id' or 'dict_connection must be specified'")

        self.driver = _data['driver']
        self.host = _data['host']
        self.username = _data['username']
        self.password = _data['password']
        self.port = _data['port']
        self.database = _data['database']

        with suppress(KeyError):
            self.instance_name = _data['instance_name']

        if search(self.driver, "{MySQL}"):
            from pymysql import connect, cursors
            try:
                self.connection = connect(
                    host=self.host,
                    port=int(self.port),
                    user=self.username,
                    password=self.password,
                    database=self.database,
                    charset='utf8mb4',
                    cursorclass=cursors.DictCursor,
                    connect_timeout=timeout
                )
            except Exception as e:
                raise ConnectionException(str(e))
        elif search(self.driver, "{PostgreSQL}"):
            from psycopg2 import connect
            from psycopg2.extras import RealDictCursor
            try:
                self.connection = connect(
                    user=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    cursor_factory=RealDictCursor,
                    connect_timeout=timeout
                )
            except Exception as e:
                raise ConnectionException(str(e))
        elif 'MSSQL' in self.driver or 'SQL Server' in self.driver:
            import pyodbc

            _server = "{host}{instance_name},{port}".format(
                host=self.host,
                instance_name='\\' + self.instance_name if self.instance_name else '',
                port=self.port
            )

            str_conn = f"""
                        DRIVER={self.driver};
                        SERVER={_server};
                        DATABASE={self.database};
                        UID={self.username};
                        PWD={self.password};
                    """
            try:
                self.connection = pyodbc.connect(str_conn, timeout=timeout)
            except Exception as e:
                raise ConnectionException(str(e))
        else:
            raise NotImplementedError(
                f'It has not been defined how to handle the supplied controller: {self.driver}')

    def execute_query(
        self, bucket: str = None, file: str = None,
        query: str = None,
        params={},
        results=Results.DICT
    ):
        """
            Execute the statement (it can be a '.sql' file or string with the query) with the specified connection.

            :param bucket: Arn from the s3 Bucket
                You must first make sure that you have the permissions on the resource to invoke
            :type bucket: string

            :param file: file name with extension
                You must first make sure that you have the permissions on the resource to invoke
            :type file: strings

            :param query: query string to be executed
            :type query: string

            :param params: parameters to be replaced as statement in query as statement
            :type params: object

            :param results:Types of expected results
            :type results: NeoConnector.extras.Results

            :raises
                ValueError: If bucket is None ad file is None or query is None.
                NoSuchConnectionException: When trying to run a query and the connection does not exist.
                QueryingException: When you try to run a query, but it is invalid.

            :return: Dictionary list with query results
        """

        is_file = not ((bucket is None) and (file is None))
        is_script = not (query is None)

        if is_file or is_script:
            if bucket and file:
                query = get_script_content(bucket, file)
            try:
                query = query.format(*params, **params)

                data = pd.read_sql_query(
                    query, self.connection, coerce_float=False)

                if results is Results.DICT:
                    return data.to_dict(orient='records')
                elif results is Results.JSON:
                    return data.to_json(orient='records')
                else:
                    return data
            except AttributeError as e:
                raise NoSuchConnectionException(str(e))
            except Exception as e:
                raise QueryingException(str(e))
        else:
            raise ValueError('"Bucket" and "file" or "query" must not be null')
