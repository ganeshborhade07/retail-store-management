import logging
import copy
from datetime import date, datetime
from models import BillItem, Item, Transaction
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from utils.constants import ERROR_CODES, RESPONSE

logger = logging.getLogger(__name__)

class SalesSummaryHelper:
    def __init__(self, session):
        self.session = session
    
    async def get_sales_data(self, *args, **kwargs):
        try:
            response = copy.deepcopy(RESPONSE["api"])
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            
            if start_date > end_date:
                response["message"] = "end date should not be grater than start date"
                return response
            
            quantity_per_item = self.session.query(
                    BillItem.item_code,
                    func.sum(BillItem.quantity).label('total_quantity')
                ).join(Transaction, BillItem.transaction_id == Transaction.id
                ).filter(Transaction.business_day.between(start_date, end_date)
                ).group_by(BillItem.item_code
                ).all()
                
            sales_amount_per_item = self.session.query(
                    BillItem.item_code,
                    func.sum(BillItem.quantity * BillItem.price).label('total_sales_amount')
                ).join(Transaction, BillItem.transaction_id == Transaction.id
                ).filter(Transaction.business_day.between(start_date, end_date)
                ).group_by(BillItem.item_code
                ).all()
                
            quantity_sales_per_category = self.session.query(
                    Item.category,
                    func.sum(BillItem.quantity).label('total_quantity'),
                    func.sum(BillItem.quantity * Item.price).label('total_sales_amount')
                ).join(
                    Item, BillItem.item_code == Item.code
                ).join(
                    Transaction, BillItem.transaction_id == Transaction.id
                ).filter(
                    Transaction.business_day.between(start_date, end_date)
                ).group_by(
                    Item.category
                ).all()
                
            results = {
                    "quantity_per_item": [{'item_code': item[0], 'total_quantity': item[1]} for item in quantity_per_item],
                    "sales_amount_per_item": [{'item_code': item[0], 'total_sales_amount': item[1]} for item in sales_amount_per_item],
                    "quantity_sales_per_category": [{'item_code': item[0], 'total_quantity': item[1], 'total_sales_amount': item[2]} for item in quantity_sales_per_category],
                }

            response["success"] = True
            response['result'] = results
            response["http_status_code"] = 200

        except Exception as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["general_exception"]["code"]
            response["error"]["message"] = ERROR_CODES["general_exception"]["message"].format(e)

        return response
    
    
    async def average_sales_data(self, *args, **kwargs):
        try:
            response = copy.deepcopy(RESPONSE["api"])
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            
            if start_date > end_date:
                response["message"] = "end date should not be grater than start date"
                return response
                
            quantity_sales_per_category = self.session.query(
                    Item.category,
                    func.sum(BillItem.quantity).label('total_quantity'),
                    func.sum(BillItem.quantity * Item.price).label('total_sales_amount'),
                    func.count(BillItem.item_code).label('item_count')
                ).join(
                    Item, BillItem.item_code == Item.code
                ).join(
                    Transaction, BillItem.transaction_id == Transaction.id
                ).filter(
                    Transaction.business_day.between(start_date, end_date)
                ).group_by(
                    Item.category
                ).all()
                
            averages = []
            for row in quantity_sales_per_category:
                category, total_quantity, total_sales_amount, item_count = row
                average_quantity = total_quantity / item_count
                average_sales_amount = total_sales_amount / item_count
                averages.append({
                    'category': category,
                    'average_quantity': float(average_quantity),
                    'average_sales_amount': float(average_sales_amount)
                })

            response["success"] = True
            response['result'] = averages
            response["http_status_code"] = 200

        except Exception as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["general_exception"]["code"]
            response["error"]["message"] = ERROR_CODES["general_exception"]["message"].format(e)

        return response
