from bson import ObjectId
from app.db.connect.mongo import get_sync_engine

sync_engine = get_sync_engine()


def fetch_database_model(modelClass, obj_id: ObjectId): # type: ignore
    # SYNC Mongo engine is used because Pydantic validation in synchrone
    data = sync_engine.find_one(modelClass, modelClass.id == obj_id) # type: ignore
    if not data:
        raise ValueError(
            "No %s found with ObjectId(%s)" % (modelClass.__name__, obj_id) # type: ignore
        )

    res = data.dict() # type: ignore
    res["id"] = str(res["id"])  # type: ignore # convert ObjectId to str
    return res # type: ignore


class ModelObjectId(ObjectId):
    """
    This is a ODMantic / Pydantic custom field type
        ODMantic Doc : https://art049.github.io/odmantic/fields/#custom-field-types
        Pydantic Doc : https://docs.pydantic.dev/latest/usage/types/custom/#as-a-method-on-a-custom-type

    This Class in a parent Class. DO NOT USE IT DIRECTLY
    """

    _model = None  # used for heritage to define DB Model to fetch

    @classmethod
    def __get_validators__(cls): # type: ignore
        yield cls.validate # type: ignore

    @classmethod
    def validate(cls, v): # type: ignore
        # Security : do not use this Class direclty
        if cls._model == None:
            raise ValueError("No model provided")

        # Handle data coming from FastAPI request
        if isinstance(v, str):
            return ObjectId(v)

        # Handle data coming from MongoDB
        if isinstance(v, ObjectId):
            # SYNC engine for validation
            return fetch_database_model(cls._model, v)

        raise ValueError("%s data validation error" % (cls.__name__))
