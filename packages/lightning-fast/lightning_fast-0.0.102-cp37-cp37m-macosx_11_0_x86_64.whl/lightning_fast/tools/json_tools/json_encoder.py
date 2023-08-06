import json

from lightning_fast.tools.json_tools.encoders.mongodb_doc_encoder import (
    MongodbDocEncoder,
)


class JsonEncoder:
    @classmethod
    def encode_mongodb(cls, mongodb_doc):
        return json.dumps(mongodb_doc, cls=MongodbDocEncoder)
