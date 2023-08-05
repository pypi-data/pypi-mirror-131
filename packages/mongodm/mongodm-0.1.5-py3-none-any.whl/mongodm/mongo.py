import pymongo
from pymongo.collection import Collection as PymongoCollection
from pymongo.database import Database as PymongoDatabase


class MongoClient(pymongo.MongoClient):
    def __call__(self, database: str):
        return self.__getattr__(database)

    def __getitem__(self, database: str) -> "Database":
        return Database(self, database)


class Database(PymongoDatabase):
    def __call__(self, collection: str):
        return self.__getattr__(collection)

    def __getitem__(self, collection: str) -> "Collection":
        return Collection(self, collection)


class Collection(PymongoCollection):
    pass
