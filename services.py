from database import db

import requests

def getReturnCode(link:[int, str, int]):
	ret = requests.get("https://" + link[1])
	return (link[0], ret.status_code, link[2])

def getReturnCodes(links:[(str,int)]):
	codes = []
	for link in links:
		codes.append(getReturnCode(link))

	print(codes)
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
	print("Start refresh")
	sites = getWebsitesFromDB()
	print("Middle 1")
	codes = getReturnCodes(sites)
	print("Middle 2")
	writeReturnCodes(codes)
	print("end refresh")
	return None
