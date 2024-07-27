from fastapi import APIRouter

from apis.v1.items_details import ItemHandlers
from .handlers import ping, ping_ready

router = APIRouter()

router.add_api_route("/ping/", ping, methods=["GET"])
router.add_api_route("/ping/ready", ping_ready, methods=["GET"])

router.add_api_route("/items", ItemHandlers.get_items, methods=["GET"])

