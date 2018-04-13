from cassandra.cluster import Cluster
from cqlengine import columns
from cqlengine.models import Model
from cqlengine.management import sync_table
from cqlengine import connection
import csv

# All of the select queries must be made in lower case, since each of the rows, when created, are made in lower case.
# Using keyspace: truncate tablename; to delete every single row from a table.
# Use clientid 309 for testing purposes.

shoppingCart = []

def chooseProduct(clientUser, errandid):
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect("shop")
	index = 1
	categoryNames = session.execute("select categoryname from product")
	categoryList = []
	productNames = session.execute("select productname, categoryname from product")
	productList = []
	print("\nCategorias")
	for category in categoryNames:
		if(category.categoryname not in categoryList):
			print("{}. {}".format(index, category.categoryname))
			categoryList.append(category.categoryname)
			index = index + 1
	option = input("\nEscoja una de las opciones previas: ")
	choose = categoryList[option - 1]
	print("\nProductos")
	index = 1
	for product in productNames:
		if(product.categoryname == choose):
			productList.append(product.productname)
			print("{}. {}".format(index, product.productname))
			index = index + 1
	option = input("\nEscoja una de las opciones previas: ")
	choose = productList[option - 1]
	quantity = input("Indique la cantidad a comprar: ")
	session.execute("""
		insert into errand(errandid, clientid, errandstate, erranddate, errandquantity)
		""")
	del productList[:]
	del categoryList[:]
	return choose, quantity, errandid

def options():
	errandid = 1
	print("""
		1. Ver mi carrito de compras.
		2. 
		""")
	option = input("Escoja una de las opciones previas: ")
	if(option == 1):
		print("""
			1. Agregar producto.
			2. Remover producto.
			3. Ver los productos.
			""")
		option = input("Escoja una de las opciones previas: ")
		if(option == 1):
			productQuantity = chooseProduct(309, errandid)
			for i in range(productQuantity[1]):
				shoppingCart.append(productQuantity[0])


def main():
	options()

main()


# def main():
# 	cluster = Cluster(['127.0.0.1'])
# 	session = cluster.connect("shop")
# 	session.execute("""
# 		insert into client(clientid, clientname, clientaddress, clientemail, clientusername, clientpassword)
# 		values (11234, 'John', 'Kra 5', 'hotmail', 'foo', 'bar')
# 		""")
# 	session.execute("""
# 		insert into client(clientID, clientName, clientAddress, clientEmail, clientUsername, clientPassword)
# 		values (5739, 'Karl', 'Kra55', 'hotmail', 'foobar', 'barfoo')
# 		""")
# 	session.execute("""
# 		delete from client where clientid = 5739
# 		""")
# 	# result = session.execute("select clientID, clientName from client")
# 	# for i in result:
# 	# 	print(i.clientid)


# tupleChosen = chooseProduct()
# print(tupleChosen[0])