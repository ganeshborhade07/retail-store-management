import ujson
import logging
from config import current_config
from database import Backend
from fastapi import FastAPI, Response
from apis.v1.urls import router as api_router

logger = logging.getLogger(__name__)

class RetailApp(object):
    def __init__(self, current_config):
        self.current_config = current_config
    
    @staticmethod
    def create_app(app):
        backend = Backend.instance()
        swagger_json = {}
        app.include_router(api_router, prefix='/v1.0')
        return app
