import psycopg2
import dbSecret

class Database:
	def __init__(self):
		self.lock = False
		self.conn = self.connect()
		self.cur = self.conn.cursor()

	def __del__(self):
		if hasattr(self, "cur"):
			self.cur.close()
		if hasattr(self, "conn"):
			self.conn.close()

	def connect(self):
		conn = psycopg2.connect(
			user = dbSecret.dbusername, 
			password = dbSecret.dbpassword,
			host = dbSecret.dbhost,
			port = dbSecret.dbport,
			dbname = dbSecret.dbname 
		)
		return conn

	def createTables(self):
		self.cur.execute("""
			CREATE TABLE websites (
				id serial PRIMARY KEY,
				url TEXT NOT NULL,
				shouldReturn INT
			)
		""")
	
		self.cur.execute("""
			CREATE TABLE websiteStatus (
				id serial PRIMARY KEY,
				urlId INTEGER REFERENCES websites(id),
				statusCode INT,
				timeStamp TIMESTAMP
			)
		""")

		self.conn.commit()

	def getUrls(self):
		self.cur.execute( "SELECT * FROM websites" )
		return self.cur.fetchall()

	def addUrl(self, url, status):
		while self.lock:
			pass

		self.lock = True
		self.cur.execute(
			"INSERT INTO websites (url, shouldReturn) VALUES (%s, %s)",
			(url, status,)
		)
		self.conn.commit()
		self.lock = False

	def deleteUrl(self, urlId):
		while self.lock:
			pass
		self.lock = True

		ret = self.cur.execute(
			"DELETE FROM websites WHERE id = %s",
			(urlId,)
		)
		self.conn.commit()
		self.lock = False

	def addStatus(self, urlId, status):
		while self.lock:
			pass
		self.lock = True

		self.cur.execute(
			"INSERT INTO websiteStatus (urlId, statusCode, timeStamp) VALUES (%s, %s, NOW())",
			(urlId, status,)
		)
		self.conn.commit()

		self.lock = False

	def getStatsFromId(self, urlId):
		self.cur.execute(
			"SELECT statusCode, timeStamp FROM websiteStatus WHERE urlId = %s",
			(urlId,)
		)
		return self.cur.fetchall()

	def getStatuses(self):
		self.cur.execute(
			"SELECT * FROM websiteStatus"
		)
		return self.cur.fetchall()

	def getLastStatuses(self):
		self.cur.execute(
			"SELECT * FROM websiteStatus WHERE id IN (SELECT MAX(id) as id FROM websiteStatus GROUP BY urlid)"
		)
		return self.cur.fetchall()

	def getLastStatusesWithNames(self):
		self.cur.execute(
			"SELECT websites.url, websiteStatus.statusCode, websites.id FROM websiteStatus INNER JOIN websites ON websitestatus.urlid = websites.id WHERE websitestatus.id IN (SELECT MAX(id) as id FROM websiteStatus GROUP BY urlid);"
		)
		return self.cur.fetchall()

	def getUrlFromId(self, websiteId):
		self.cur.execute(
			"SELECT * FROM websites WHERE id = %s",
			(websiteId,)
		)
		return self.cur.fetchall()

db = Database()
