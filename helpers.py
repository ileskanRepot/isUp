from database import db

def addUrl(url, status):
	db.addUrl(url, status)

def deleteUrl(urlId, status):
	db.deleteUrl(urlId)

def addStatus(urlId, status):
	db.addStatus(urlId, status)
