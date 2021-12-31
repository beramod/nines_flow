from src.db.mongodb import MongoDB
from src.api import settings

class SoulDB:
    prod_db: MongoDB = None
    temp_db = None
    dev_db = None
    env = settings.ENV

    @classmethod
    def get_prod_db(cls) -> MongoDB:
        if not cls.prod_db:
            if cls.env == "PROD":
                uris = '{hot db info}'
            else:
                uris = "mongodb://127.0.0.1:20022,127.0.0.1:20023,127.0.0.1:20024"

            cls.prod_db = MongoDB(uris)
        return cls.prod_db

    @classmethod
    def get_temp_db(cls) -> MongoDB:
        if not cls.temp_db:
            if cls.env == "PROD":
                uris = '{cache db info}'
            else:
                uris = "mongodb://127.0.0.1:20032"
            cls.temp_db = MongoDB(uris)
        return cls.temp_db

    @classmethod
    def get_dev_db(cls) -> MongoDB:
        if not cls.dev_db:
            uris = "{dev db info}"
            cls.dev_db = MongoDB(uris)
        return cls.dev_db
