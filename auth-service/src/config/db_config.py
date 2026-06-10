"""
The DbConfig class.
module: src/config/db_config.py
"""


class DbConfig:
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.uri = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
