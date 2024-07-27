import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

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
