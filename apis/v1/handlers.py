import logging
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from database import Backend

app = FastAPI()
logger = logging.getLogger(__name__)

class responses:
    class Ok:
        status_code = 200

async def ping():
    status = responses.Ok.status_code
    ready = True
    message = "available service" if ready else "Not ready"
    return JSONResponse(content={"success": ready, "msg": message}, status_code=status)

async def ping_ready():
    status = responses.Ok.status_code
    ready = True
    message = "available service" if ready else "service Not available"
    return JSONResponse(content={"success": ready, "msg": message}, status_code=status)

class BaseHandler:
    def __init__(self, request: Request):
        self.request = request
    
    @property
    def backend(self):
        return Backend.instance()
    
    def load_json(self):
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            raise HTTPException(400, msg)
