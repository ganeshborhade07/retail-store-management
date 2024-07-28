import logging
from fastapi import Request
from marshmallow import ValidationError
from database import Backend
from helper.sales_helper import SalesSummaryHelper
from serialiser.serialiser import SalesSummarySchema

logger = logging.getLogger(__name__)
session = Backend().get_session()


class SalesHandlers:
    def __init__(self) -> None:
        self.session = session
        
    async def fetch_sales(request: Request):
        try:
            data = await request.json()
            schema = SalesSummarySchema()
            validated_data = schema.load(data)
            
            sales_helper = SalesSummaryHelper(session)
            sales_data = await sales_helper.get_sales_data(**validated_data)
        except ValidationError as err:
            logger.exception("Validation error: %s", err.messages)
            sales_data = {"message": "Invalid input", "errors": err.messages}
        except Exception as e:
            logger.exception("Exception: %s", e)
            sales_data = {"message": "something went wrong"}
        return sales_data
    
    async def average_sales_data(request: Request):
        try:
            data = await request.json()
            schema = SalesSummarySchema()
            validated_data = schema.load(data)
            
            sales_helper = SalesSummaryHelper(session)
            average_sales_data = await sales_helper.average_sales_data(**validated_data)
        except ValidationError as err:
            logger.exception("Validation error: %s", err.messages)
            average_sales_data = {"message": "Invalid input", "errors": err.messages}
        except Exception as e:
            logger.exception("Exception: %s", e)
            average_sales_data = {"message": "something went wrong"}
        return average_sales_data

    
    async def generate_sales_data(request: Request):
        try:
            data = await request.json()
            schema = SalesSummarySchema()
            validated_data = schema.load(data)
            sales_helper = SalesSummaryHelper(session)
            generate_sales_data = await sales_helper.generate_sales_report(**validated_data)
        except ValidationError as err:
            logger.exception("Validation error: %s", err.messages)
            generate_sales_data = {"message": "Invalid input", "errors": err.messages}
        except Exception as e:
            logger.exception("Exception: %s", e)
            generate_sales_data = {"message": "something went wrong"}
        return generate_sales_data
