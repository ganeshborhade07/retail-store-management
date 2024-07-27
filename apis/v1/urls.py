from fastapi import APIRouter

from apis.v1.items_details import ItemHandlers
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
