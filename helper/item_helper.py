import logging
import copy
from models import Item
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from utils.constants import ERROR_CODES, RESPONSE

logger = logging.getLogger(__name__)

class ItemHelper:
    def __init__(self, session):
        self.session = session
    
    async def get_all_items(self, *args, **kwargs):
        try:
            res = list()
            response = copy.deepcopy(RESPONSE["api"])
            item_obj = self.session.query(Item).all()
            for item in item_obj:
                item_response = {
                        "name" : item.name,
                        "remaining_quantity" : item.starting_quantity,
                        "price" : item.price,
                    }
                res.append(item_response)
            logger.info('All items object query')
            
            response["message"] = "successfully fetch items"
            response["result"] = res
            response["success"] = True
            response["http_status_code"] = 200

        except Exception as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["general_exception"]["code"]
            response["error"]["message"] = ERROR_CODES["general_exception"]["message"].format(e)

        return response
    
    async def get_item(self, name, *args, **kwargs):
        try:
            res = []
            response = copy.deepcopy(RESPONSE["api"])
            if not name:
                return {"message": "name not found in header"}
            name = name.lower()
            item_obj = self.session.query(Item).filter(
                    (func.lower(Item.name) == name.lower()) | 
                    (func.lower(Item.code) == name.lower()) | 
                    (func.lower(Item.category) == name.lower())
                ).all()
            
            if not item_obj:
                return {"message": "item not found"}
            
            for item in item_obj:
                item_response = {
                        "name" : item.name,
                        "remaining_quantity" : item.starting_quantity,
                        "price" : item.price,
                    }
                res.append(item_response)

            logger.info('item object query')
            
            response["message"] = "successfully fetch items"
            response["result"] = res
            response["success"] = True
            response["http_status_code"] = 200
            
        except NoResultFound as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["db"]["code"]
            response["error"]["message"] = ERROR_CODES["db"]["message"].format(e)
            response["message"] = f"no row was found"
        
        except Exception as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["general_exception"]["code"]
            response["error"]["message"] = ERROR_CODES["general_exception"]["message"].format(e)
        return response
        
