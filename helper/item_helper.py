import logging
import copy
from models import Item
from utils.constants import ERROR_CODES, RESPONSE

logger = logging.getLogger(__name__)

class ItemHelper:
    def __init__(self, session):
        self.session = session
    
    async def get_all_items(self):
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
            self.set_status(ERROR_CODES["general_exception"]["http_response_status_code"])

        return response
