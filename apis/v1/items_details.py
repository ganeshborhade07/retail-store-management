import logging
from fastapi import Request
from helper.item_helper import ItemHelper

from database import Backend

logger = logging.getLogger(__name__)
session = Backend().get_session()


class ItemHandlers:
    
    async def get_items():
        item_helper = ItemHelper(session)
        items = await item_helper.get_all_items()
        return items

    # async def get_item(item_id: int, db: Session = Depends(get_db)):
    #     item = db.query(Item).filter(Item.id == item_id).first()
    #     if not item:
    #         raise HTTPException(status_code=404, detail="Item not found")
    #     return item
