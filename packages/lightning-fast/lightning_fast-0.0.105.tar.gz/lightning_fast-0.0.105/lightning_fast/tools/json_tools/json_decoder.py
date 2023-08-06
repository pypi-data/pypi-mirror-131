import json

from lightning_fast.tools.json_tools.decoders.mongodb_doc_decoder import (
    MongodbDocDecoder,
)


class JsonDecoder:
    @classmethod
    def decode_mongodb(cls, mongodb_string):
        return json.loads(
            mongodb_string, cls=MongodbDocDecoder,
        )
