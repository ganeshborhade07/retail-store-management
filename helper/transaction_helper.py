import logging
import copy
from datetime import date, datetime
from common.decorator import measure_latency
from models import Item, Transaction
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from utils.constants import ERROR_CODES, RESPONSE

logger = logging.getLogger(__name__)

class TransactionHelper:
    def __init__(self, session):
        self.session = session
    
    @measure_latency
    async def create_transaction(self, *args, **kwargs):
        try:
            item_obj = None
            current_day = date.today()
            current_timestamp = datetime.now()
            response = copy.deepcopy(RESPONSE["api"])
            item_code = kwargs.get('code')
            try:
                item_obj = self.session.query(Item).filter(Item.code == item_code).one()
            except Exception as e:
                pass
            
            if item_obj:
                response['message'] = f"{item_code} is already present"
                response["success"] = False
                response["http_status_code"] = 400
                return response
            
            new_transaction = Transaction(
                            business_day=current_day,
                            timestamp=current_timestamp
                        )
            new_item = Item(**kwargs)

            self.session.add(new_transaction)
            self.session.add(new_item)  
            self.session.commit()
            
            logger.info('transaction and item inserted successfully')
            
            response["message"] = "transaction and item inserted successfully"
            response["success"] = True
            response["http_status_code"] = 200

        except Exception as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["general_exception"]["code"]
            response["error"]["message"] = ERROR_CODES["general_exception"]["message"].format(e)

        return response
    
