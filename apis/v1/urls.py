from fastapi import APIRouter

from apis.v1.items_details import ItemHandlers
from apis.v1.sales_summary import SalesHandlers
from apis.v1.transaction import TransactionHandlers
from .handlers import ping, ping_ready

router = APIRouter()

router.add_api_route("/ping/", ping, methods=["GET"])
router.add_api_route("/ping/ready", ping_ready, methods=["GET"])

# items api
router.add_api_route("/items", ItemHandlers.get_items, methods=["GET"])
router.add_api_route("/items/{name}", ItemHandlers.get_single_item, methods=["GET"])

# transaction
router.add_api_route("/transaction", TransactionHandlers.create_transaction, methods=["POST"])

# sales summary
router.add_api_route("/sales-summary", SalesHandlers.fetch_sales, methods=["POST"])

# average sales data
router.add_api_route("/avg/sales/data", SalesHandlers.average_sales_data, methods=["POST"])

# generate sales report
router.add_api_route("/generate/sales-report", SalesHandlers.generate_sales_data, methods=["POST"])
