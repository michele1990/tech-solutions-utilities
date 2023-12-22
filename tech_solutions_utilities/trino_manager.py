# trino_manager

import pandas as pd
import trino
from trino import dbapi
from trino.auth import BasicAuthentication, OAuth2Authentication

class TrinoManager:
    def __init__(self, host, port, user=None, password=None, use_local_auth=False):
        self.host = host
        self.port = port

        if use_local_auth:
            # Local testing with OAuth2 authentication (opens browser)
            self.auth = OAuth2Authentication()
        else:
            # Deployment with Basic authentication (user and password provided)
            self.auth = BasicAuthentication(user, password) if user and password else None

    def execute_query(self, query, fetch_pandas=False):
        conn_details = {
            'host': self.host,
            'port': self.port,
            'http_scheme': 'https',
            'auth': self.auth
        }

        with dbapi.connect(**conn_details) as conn:
            if fetch_pandas:
                return pd.read_sql_query(query, conn)
            else:
                cur = conn.cursor()
                cur.execute(query)
                return cur.fetchall()
