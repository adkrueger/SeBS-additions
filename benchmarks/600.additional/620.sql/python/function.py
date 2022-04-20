import sys
import datetime
import pymysql


def handler(event):
	db_username = "admin"
	db_password = "Password_cs525"
	db_name = "sys"
	db_endpoint = "cs525db.ccdmy6t17hxh.us-east-1.rds.amazonaws.com"

	try:
		conn = pymysql.connect(host=db_endpoint, user=db_username, passwd=db_password, db=db_name, connect_timeout=5)
	except Exception as e:
		logger.error("ERROR: Unexpected error: Could not connect to MySql instance:")
		print(e)
		sys.exit()

	processing_begin = datetime.datetime.now()
	# perform a couple of SQL commands, then store some of the results in another table
	with conn.cursor() as c:
		# get the distinct city1 names across the two joined tables where balance > 100000
		statement1 = "select distinct c1.name from sys.city1 as c1 \
				inner join sys.city2 as c2 on c1.name = c2.name \
				where c1.balance > 100000 or c2.balance > 100000;"
		# get the sum of balances for names across the 2 cities who have balances < 50000
		statement2 = "select name, sum(balance) \
				from (select c1.name, c1.balance + c2.balance as balance from sys.city1 as c1 \
				inner join sys.city2 as c2 on c1.id = c2.id \
				where c1.balance < 50000 and c2.balance < 50000 \
				group by c1.name) as x \
				group by name;"
		
		c.execute(statement1);
		s1_results = c.fetchall();

		# delete stuff from the third table in case it's full from a previous run
		c.execute("delete from sys.results;")
		conn.commit()

		# add the results of statement1
		temp_int = 0
		for r in s1_results:
			temp_int += 1
			c.execute(f"insert into sys.results (count, total, temp) values ({temp_int}, 0, '{r[0]}');")
		conn.commit()
		
		c.execute(statement2);
		s2_results = c.fetchall();

		# add the results of statement2
		temp_int = 0
		for r in s2_results:
			temp_int += 1
			c.execute(f"insert into sys.results (count, total, temp) values ({temp_int}, {r[1]}, '{r[0]}');")
		conn.commit()
	processing_end = datetime.datetime.now()

	processing_time = (processing_end - processing_begin) / datetime.timedelta(microseconds=1)
	num_entries = 20000*20000

	return {
		'result': 'success!',
		'measurement': {
			'processing_time': processing_time,
			'num_entries': num_entries
		}
	}


