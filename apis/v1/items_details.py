import logging
from fastapi import Request
from helper.item_helper import ItemHelper

from database import Backend

logger = logging.getLogger(__name__)
session = Backend().get_session()


class ItemHandlers:
    def __init__(self) -> None:
        self.session = session
        
    async def get_items():
        try:
            item_helper = ItemHelper(session)
            items = await item_helper.get_all_items()
        except Exception as e:
            logger.exception(e)
            items = {"message": "something went wrong"}
        return items

    async def get_single_item(name):
        try:
            item_helper = ItemHelper(session)
            item = await item_helper.get_item(name)
        except Exception as e:
            logger.exception(e)
            item = {"message": "something went wrong"}
        return item
