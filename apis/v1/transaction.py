import logging
from fastapi import Request
from helper.transaction_helper import TransactionHelper
from marshmallow import ValidationError

from database import Backend
from serialiser.serialiser import ItemSchema

logger = logging.getLogger(__name__)
session = Backend().get_session()


class TransactionHandlers:
    def __init__(self) -> None:
        self.session = session
        
    async def create_transaction(request: Request):
        try:
            data = await request.json()
            schema = ItemSchema()
            validated_data = schema.load(data)
            
            transaction_helper = TransactionHelper(session)
            items = await transaction_helper.create_transaction(**validated_data)
        except ValidationError as err:
            logger.exception("Validation error: %s", err.messages)
            items = {"message": "Invalid input", "errors": err.messages, "success": False}
        except Exception as e:
            logger.exception("Exception: %s", e)
            items = {"message": "something went wrong"}
        return items
