import psycopg2
import requests
import bcrypt

from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import services

# from database import db
# from helpers import addStatus, addUrl

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
	statuses = services.getLastStatusesWithNames()
	print(statuses)
	return templates.TemplateResponse("overview.html", {"request": request, "urls": statuses})

@app.get("/{websiteId}")
async def read_item(request: Request, websiteId: int):
	name = services.getUrlFromId(websiteId)
	stats = services.getStatsFromId(websiteId)
	print(stats)
	return templates.TemplateResponse("induvidual.html", {"request": request, "url": name, "stats": stats})

# @app.get("/login")
# async def root(request: Request):
	# statuses = services.getLastStatusesWithNames()
	# return {"qwf":"123"}

@app.post("/refresh", response_class=RedirectResponse, status_code=303)
async def refresh(request: Request):
	services.refreshPages()
	return "/"

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
# 	response = await call_next(request)
# 	return response