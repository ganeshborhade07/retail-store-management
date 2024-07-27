import asyncio
import logging

import uvloop
from fastapi import FastAPI
import uvicorn
from config import current_config
from retail_app import RetailApp

logger = logging.getLogger(__name__)

fast_api_app = FastAPI()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

retail_app = RetailApp(current_config)
app = RetailApp.create_app(fast_api_app)

if current_config.DEBUG:
    current_config.SERVER_WORKERS = 1

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=current_config.PORT,
        reload=current_config.DEBUG, 
        workers=current_config.SERVER_WORKERS,
        log_level="info"
    )
