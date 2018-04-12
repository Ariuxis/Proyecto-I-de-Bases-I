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
	errandState set<text>,
	errandQuantity int
);

create table if not exists bill (
	billID int primary key,
	billCard set<text>,
	errandID int,
	cardID int,
	approvalID int,
	cardEntity int
);

# WIP tables may not be completed. Further reading into this.