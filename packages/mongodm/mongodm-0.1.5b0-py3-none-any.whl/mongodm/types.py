from typing import Any, Callable, Optional, Union

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo.results import DeleteResult, UpdateResult

from .mongo import Collection, Database
from .query import Q


class Id(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: ObjectId) -> ObjectId:
        return value


class Document(BaseModel):
    __collection: Collection

    id: Id = Field(default=None, alias="_id")

    @classmethod
    @property
    def __collection_name(cls) -> str:
        """Returns class name in camel case if Meta has no attribute
        collection_name or collection_name_generator.

        Returns:
            str: Class name
        """
        try:
            if hasattr(cls, "collection_name"):
                return cls.Meta.collection_name
            elif hasattr(cls, "collection_name_generator"):
                return cls.Meta.collection_name_generator(cls)
            raise AttributeError
        except AttributeError:
            name = cls.__name__
            return name[0].lower() + name[1:]

    @classmethod
    @property
    def collection(cls) -> Collection:
        """Returns a collection by class name

        Returns:
            Collection: Class collection
        """
        try:
            return cls.__collection
        except AttributeError:
            cls.__collection = cls.Meta.database(cls.__collection_name)
            return cls.__collection

    @classmethod
    @property
    def default_values(cls) -> dict:
        if not hasattr(cls, "_default_values"):
            setattr(cls, "_default_values", {})
            fields: dict = cls.__dict__["__fields__"]
            for key, value in fields.items():
                if value.default is not None:
                    cls._default_values[key] = value.default
        return cls._default_values.copy()

    @classmethod
    def filter(
        cls, query: Q = Q(), limit: int = 0, sort: Any = None, **kwargs: Any
    ) -> list["Document"]:
        """Get one or more documents from database.

        Works like `find` in pymongo.

        MongODM `filter` example:
        >>> Document.filter(hello="world")

        Pymongo `find` example:
        >>> db.test.find({"hello": "world"})

        Returns:
            list[`Document`]: Returns a `list` of documents, or empty `list`
            if no matching document is found.
        """
        return [
            cls(**data)
            for data in cls.collection.find(query, limit=limit, sort=sort, **kwargs)
        ]

    @classmethod
    def get(cls, query: Q, sort: Any = None, **kwargs: Any) -> Union["Document", None]:
        """Get a single document from the database.

        Works like `find_one` in pymongo.

        MongODM `filter` example:
        >>> Document.get(hello="world")

        Pymongo `find` example:
        >>> db.test.find_one({"hello": "world"})

        Returns:
            Union[`Document`, `None`]: Returns a single document, or `None` if no matching
            document is found.
        """
        obj = cls.collection.find_one(query, sort=sort, **kwargs)
        if not obj:
            return None

        return cls(**obj) if obj is not None else None

    @classmethod
    def create(cls, **kwargs: Any) -> "Document":
        """Create document in the class collection.

        Returns:
            `Document`: Document model with `ObjectID` and included fields.
        """
        values = cls.default_values
        values.update(kwargs)
        obj = cls.collection.insert_one(values).inserted_id
        return cls(_id=obj, **kwargs)

    @classmethod
    def create_many(
        cls, *data: dict[str, Any], in_model=False
    ) -> list[Union[ObjectId, "Document"]]:
        """Create multiple documents in the class collection.

        Returns:
            list[Union[`ObjectId`, `Document`]]: Returns `list` with `ObjectId`
            only if `in_model` is `False`, else returns `list` with `Document` model
        """
        object_ids = cls.collection.insert_many(data).inserted_ids
        if not in_model:
            return object_ids
        return [cls(id=_id, **values) for _id, values in zip(object_ids, data)]

    @classmethod
    def delete_one(cls, query: Q) -> DeleteResult:
        """Delete document in the class collection.

        Returns:
            DeleteResult: Delete result from Pymongo.
        """
        return cls.collection.delete_one(query)

    @classmethod
    def delete_many(cls, query: Q = Q()) -> DeleteResult:
        """Delete multiple documents in the class collection.

        Returns:
            DeleteResult: Delete result from Pymongo.
        """
        return cls.collection.delete_many(query)

    def delete(self) -> DeleteResult:
        """Delete instance.

        Raises:
            AttributeError: Raises when instance have no id or lookup_field.

        Returns:
            DeleteResult: Delete result from Pymongo.
        """
        if ObjectId.is_valid(self.id):
            return self.collection.delete_one({"_id": self.id})
        elif hasattr(self.Meta, "lookup_field"):
            lookup_field = self.Meta.lookup_field
            lookup_value = getattr(self, lookup_field)
            return self.collection.delete_one({lookup_field: lookup_value})
        raise AttributeError(
            "The object does not have an ObjectId,"
            "set the lookup_field attribute to Meta"
        )

    @classmethod
    def update_one(cls, query: Q, **values: Any) -> UpdateResult:
        """Update document in the class collection.

        Args:
            query (Q): Query object for document filtering.

        Returns:
            UpdateResult: Update result from Pymongo.
        """
        return cls.collection.update_one(query, {"$set": values})

    @classmethod
    def update_many(cls, query: Q = Q(), **values: Any) -> UpdateResult:
        """Update multiple documents in the class collection.

        Args:
            query (Q): Query object for document filtering.

        Returns:
            UpdateResult: Update result from Pymongo.
        """
        return cls.collection.update_many(query, {"$set": values})

    def update(self, **values: Any) -> UpdateResult:
        """Update instance.

        Raises:
            AttributeError: Raises when instance have no id or lookup_field.

        Returns:
            UpdateResult: Update result from Pymongo.
        """
        if not ObjectId.is_valid(self.id) and not hasattr(self.Meta, "lookup_field"):
            raise AttributeError(
                "The object does not have an id,"
                "set the lookup_field attribute to Meta"
            )
        for key, value in values.items():
            setattr(self, key, value)
        if ObjectId.is_valid(self.id):
            return self.collection.update_one({"_id": self.id}, values)
        lookup_field = self.Meta.lookup_field
        lookup_value = getattr(self, lookup_field)
        return self.collection.update_one({lookup_field: lookup_value}, values)

    class Meta:
        database: Database
        collection_name: Optional[str]
        collection_name_generator: Optional[Callable]
        lookup_field: Optional[str]
