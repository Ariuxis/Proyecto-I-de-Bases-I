/* Run script as following:
 * Log into cqlsh shell with the following command: cqlsh
 * Run the following command: source '~/mydir/myscript.cql'
 * In the developer's case, this is as following: source '~/Desktop/Universidad/BasesI/databases.cql'
 * Quitting the cqlsh shell: exit
 */

create keyspace if not exists shop with replication = {
	'class' : 'SimpleStrategy',
	'replication_factor' : 1
};

use shop;

create table if not exists client (
	clientID int primary key,
	clientName text,
	clientAddress text,
	clientEmail text,
	clientUsername text,
	clientPassword text
);

create table if not exists product (
	productID int primary key,
	categoryName text,
	productName text,
	productPrice int
);

create table if not exists errand (
	errandID int primary key,
	clientID int,
	errandState text,
	erranddate date,
	billdate date,
	errandQuantity int,
	billCard text,
	cardID int,
	approvalID int,
	cardEntity int,
	productID set<int>
);

copy client from 'cliente.csv' with delimiter = ';' and header = true;
copy product from 'producto.csv' with delimiter = ',' and header = true;