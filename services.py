from multiprocessing import Pool
from database import db

import requests

def getReturnCode(link:[int, str, int]):
	ret = requests.get("https://" + link[1])
	# print(ret.text)
	return (link[0], ret.status_code, link[2])

def getReturnCodes(links:[(str,int)]):
	with Pool() as pool:
		codes = pool.map(getReturnCode, links)
	return codes

def getWebsitesFromDB():
	return db.getUrls()

def getUrlFromId(urlId:int):
	return db.getUrlFromId(urlId)[0]

def getStatsFromId(urlId:int):
	return db.getStatsFromId(urlId)

def getLastStatuses():
	return db.getLastStatuses()

def getLastStatusesWithNames():
	return db.getLastStatusesWithNames()

def writeReturnCodes(codes:[[int, str, int]]):
	for code in codes:
		db.addStatus(code[0], code[1])

def refreshPages():
	sites = getWebsitesFromDB()
	codes = getReturnCodes(sites)
	writeReturnCodes(codes)