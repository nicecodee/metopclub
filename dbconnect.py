import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost", user="root", passwd="jxlgood", db="metopclub")
	c = conn.cursor()
	return c, conn