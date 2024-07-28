import logging
import copy
import json
from database import Backend
from models import Item
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from utils.constants import ERROR_CODES, RESPONSE

logger = logging.getLogger(__name__)

class ItemHelper:
    def __init__(self, session):
        self.session = session
        self.redis = Backend().get_redis()

    async def get_all_items(self, *args, **kwargs):
        try:
            res = list()
            response = copy.deepcopy(RESPONSE["api"])
            cached_items = self.redis.get("get_all_items")
            if cached_items:
                res = json.loads(cached_items)
            else:
                item_obj = self.session.query(Item).all()
                for item in item_obj:
                    item_response = {
                            "name" : item.name,
                            "remaining_quantity" : item.total_quantity,
                            "price" : item.price,
                        }
                    res.append(item_response)
                self.redis.set("get_all_items", json.dumps(res))
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
            
            cached_item = self.redis.get(name)
            if cached_item:
                res = json.loads(cached_item)
            else:
                item_obj = self.session.query(Item).filter(
                        (func.lower(Item.name) == name.lower()) | 
                        (func.lower(Item.code) == name.lower()) | 
                        (func.lower(Item.category) == name.lower())
                    ).all()
            
                if not item_obj:
                    return {"message": "item not found", "success" : False}

                for item in item_obj:
                    item_response = {
                            "name" : item.name,
                            "remaining_quantity" : item.total_quantity,
                            "price" : item.price,
                        }
                    res.append(item_response)
                self.redis.set(name, json.dumps(res))

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
        
