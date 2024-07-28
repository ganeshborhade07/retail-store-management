import logging
import copy
import io
import csv
import json
from datetime import date, datetime
from database import Backend
from models import BillItem, Item, Transaction
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from fastapi.responses import StreamingResponse
from utils.constants import AVG_SALES_DATA_REDIS_KEY, ERROR_CODES, RESPONSE, SALES_DATA_REDIS_KEY

logger = logging.getLogger(__name__)

class SalesSummaryHelper:
    def __init__(self, session):
        self.session = session
        self.redis = Backend().get_redis()
    
    async def get_sales_data(self, *args, **kwargs):
        try:
            response = copy.deepcopy(RESPONSE["api"])
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            
            if start_date > end_date:
                response["message"] = "end date should not be grater than start date"
                return response
            cached_data = self.redis.get(SALES_DATA_REDIS_KEY.format(start_date=start_date, end_date=end_date))
            if cached_data:
                results = json.loads(cached_data)
            else:
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
                self.redis.set(SALES_DATA_REDIS_KEY.format(start_date=start_date, end_date=end_date), json.dumps(results))

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

            cached_data = self.redis.get(AVG_SALES_DATA_REDIS_KEY.format(start_date=start_date, end_date=end_date))
            if cached_data:
                averages = json.loads(cached_data)
            else:
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
                self.redis.set(AVG_SALES_DATA_REDIS_KEY.format(start_date=start_date, end_date=end_date), json.dumps(averages))

            response["success"] = True
            response['result'] = averages
            response["http_status_code"] = 200

        except Exception as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["general_exception"]["code"]
            response["error"]["message"] = ERROR_CODES["general_exception"]["message"].format(e)

        return response

    
    async def generate_sales_report(self, *args, **kwargs):
        try:
            response = copy.deepcopy(RESPONSE["api"])
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')

            if start_date > end_date:
                response["message"] = "end date should not be grater than start date"
                return response

            totals_query = self.session.query(
                    func.sum(BillItem.quantity).label('total_quantity'),
                    func.sum(BillItem.quantity * Item.price).label('total_sales_amount')
                ).join(
                    Item, BillItem.item_code == Item.code
                ).join(
                    Transaction, BillItem.transaction_id == Transaction.id
                ).filter(
                    Transaction.business_day.between(start_date, end_date)
                ).one()

            total_quantity = totals_query.total_quantity
            total_sales_amount = totals_query.total_sales_amount

            # Item-wise sales data
            item_sales_query = self.session.query(
                Item.code,
                Item.name,
                func.sum(BillItem.quantity).label('total_quantity'),
                func.sum(BillItem.quantity * Item.price).label('total_sales_amount')
            ).join(
                Item, BillItem.item_code == Item.code
            ).join(
                Transaction, BillItem.transaction_id == Transaction.id
            ).filter(
                Transaction.business_day.between(start_date, end_date)
            ).group_by(
                Item.code
            ).all()

            # Create CSV data
            output = io.StringIO()
            csv_writer = csv.writer(output)

            # Write headers
            csv_writer.writerow(['item_code', 'item_name', 'total_quantity', 'total_sales_amount'])

            # Write total row
            csv_writer.writerow([
                'TOTAL', '', total_quantity, total_sales_amount
            ])

            # Write average row
            item_count = len(item_sales_query)
            average_quantity = total_quantity / item_count if item_count else 0
            average_sales_amount = total_sales_amount / item_count if item_count else 0
            csv_writer.writerow([
                'AVERAGE', '', average_quantity, average_sales_amount
            ])

            # Write item-wise sales data
            for item in item_sales_query:
                csv_writer.writerow(item)

            output.seek(0)
            with open('test_sales_report.csv', 'w', newline='') as file:
                file.write(output.getvalue())

            response = StreamingResponse(
                io.BytesIO(output.getvalue().encode('utf-8')),
                media_type='text/csv',
                headers={"Content-Disposition": "attachment; filename=sales_report.csv"}
            )

        except Exception as e:
            logger.exception(e)
            response["success"] = False
            response["error"]["code"] = ERROR_CODES["general_exception"]["code"]
            response["error"]["message"] = ERROR_CODES["general_exception"]["message"].format(e)

        return response