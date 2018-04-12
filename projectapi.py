from cassandra.cluster import Cluster
from cqlengine import columns
from cqlengine.models import Model
from cqlengine.management import sync_table
from cqlengine import connection
import csv

class Client(Model):
	idClient = columns.Integer(primary_key = True)
	clientName = columns.Text()
	clientAddress = columns.Text()
	clientEmail = columns.Text()
	clientUsername = columns.Text()
	clientPassword = columns.Text()

Client.create(idClient = 11234, clientName = "John", 
	clientAddress = "Kra 5", clientEmail = "hotmail", clientUsername = "foo", clientPassword = "bar")

def main():
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect("")
	session.execute("""
		create keyspace if not exists shop with replication = {
		'class' : 'SimpleStrategy',
		'replication_factor' : 1
		} 
		""")
	session.set_keyspace("shop")
	# session.execute("""
	# 	create table if not exists client (
	# 		idClient int primary key,
	# 		clientName text,
	# 		clientAddress text,
	# 		clientEmail text,
	# 		clientUsername text,
	# 		clientPassword text
	# 	)
	# 	""")
	sync_table(Client)
	# session.execute("""
	# 	insert into client(idClient, clientName, clientAddress, clientEmail, clientUsername, clientPassword)
	# 	values (11234, 'John', 'Kra 5', 'hotmail', 'foo', 'bar')
	# 	""")
	# result = session.execute("select * from client")
	# print(result)
# main()