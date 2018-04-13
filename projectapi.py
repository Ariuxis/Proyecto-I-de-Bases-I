from cassandra.cluster import *
from cqlengine import *
from cqlengine.models import Model
from cqlengine.management import sync_table
from cqlengine import connection
import csv

# All of the select queries must be made in lower case, since each of the rows, when created, are made in lower case.
# Using keyspace: truncate tablename; to delete every single row from a table.
# Use clientid 309 for testing purposes.

shoppingCart = []

def chooseProduct(clientUser, currentErrandID):
	print("errandid: {}".format(currentErrandID))
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect("shop")
	index = 1
	totalPricing = 0
	modifyFlag = 0
	categoryNames = session.execute("select categoryname from product")
	categoryList = []
	productNames = session.execute("select productname, categoryname from product")
	productList = []
	errandQuery = session.execute("select * from errand")
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
	query = session.execute("select productprice from product where productname = %s allow filtering", (choose, ))
	for price in query:
		totalPricing = price.productprice * quantity
	for errandObject in errandQuery:
		if(errandObject.errandid == currentErrandID):
			modifyFlag = 1
			totalPricing = totalPricing + errandObject.totalprice
			session.execute("""
				update errand set errandquantity = errandquantity + %s, products = products + %s, 
				totalprice = %s where errandid = %s""",
				({quantity}, {choose}, totalPricing, currentErrandID))
	if(modifyFlag == 0):
		session.execute("""
			insert into errand(errandid, clientid, errandstate, erranddate, errandquantity, products, totalprice)
			values(%s, %s, %s, %s, %s, %s, %s)""",
			(currentErrandID, clientUser, "enProceso", "2017-04-13", {quantity}, {choose}, totalPricing))
	del productList[:]
	del categoryList[:]
	return choose, quantity

def options(currentErrandID):
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect("shop")
	print("""
		1. Ver mi carrito de compras.
		2. Salir.
		""")
	option = input("Escoja una de las opciones previas: ")
	if(option == 1):
		print("""
			1. Agregar producto.
			2. Remover producto.
			3. Ver los productos.
			4. Calcular total.
			5. Listar productos 2017.
			6. Pagar carrito.
			""")
		option = input("Escoja una de las opciones previas: ")
		if(option == 1):
			productQuantity = chooseProduct(309, currentErrandID)
			for i in range(productQuantity[1]):
				shoppingCart.append(productQuantity[0])
		elif(option == 3):
			query = session.execute("select products, errandquantity from errand where errandstate = 'enProceso' allow filtering")
			for objects in query:
				for i in range(len(objects.products)):
					print("Producto: {} / Cantidad: {}".format(objects.products[i], objects.errandquantity[i]))
		elif(option == 4):
			query = session.execute("""select totalprice from errand where clientid = %s 
				and errandState = 'enProceso' allow filtering""", (309, ))
			for price in query:
				print("Precio total del carrito: {}".format(price.totalprice))
		elif(option == 5):
			query = session.execute("""select billdate, products from errand where 
				billdate > '2017-01-01' and billdate < '2017-12-31' allow filtering""")
			for objects in query:
				print("Fecha de compra: {}".format(objects.billdate))
				for i in range(len(objects.products)):
					print("Producto: {}".format(objects.products[i]))
		elif(option == 6):
			cardType = input("Digite 1 si va a pagar con tarjeta debito, digite 2 si va a pagar con tarjeta credito: ")
			if(cardType == 1):
				cardType = "Debito"
			elif(cardType == 2):
				cardType = "Credito"
			session.execute("""
				update errand set billcard = %s, approvalid = %s, cardid = %s, billdate = %s, 
				cardentity = %s, errandState = 'Facturada' where errandid = %s""",
				(cardType, 10242, 2113, "2017-08-13", 8430, currentErrandID))
			currentErrandID = currentErrandID + 1
		options(currentErrandID)
	if(option == 2):
		return

def main():
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect("shop")
	query = session.execute("select errandid from errand")
	currentErrandID = query[0].errandid
	options(currentErrandID + 1)

main()
