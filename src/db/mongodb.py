from pymongo import MongoClient
from pymongo import ReadPreference
from pymongo import uri_parser

class MongoDB(object):
    def __init__(self, uri=None):
        self.uri = None
        self.client = None
        if uri:
            self.uri = uri
            self.client = MongoClient(uri, maxPoolSize=10, connect=False)

    def init(self):
        self.uri = None
        self.client = None

    def database(self, database_name):
        if not self.client:
            self.client = MongoClient(self.uri)
        return self.client.get_database(name=database_name, read_preference=ReadPreference.SECONDARY_PREFERRED)

    def connect(self, mongodb_uri):
        if mongodb_uri is None:
            return None
        self.uri = mongodb_uri
        parsed = uri_parser.parse_uri(mongodb_uri)
        return self.database(parsed['database'])

    def serverStatus(self):
        return self.client.server_info()

    def __getitem__(self, item):
        return self.database(item)

    def __getattr__(self, item):
        return self.database(item)
