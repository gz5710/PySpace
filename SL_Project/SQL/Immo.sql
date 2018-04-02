USE ImmoDB;

DROP Table if exists Annonce;

Create Table Annonce(
id									varchar(80) 			primary key,
title								varchar(150)		not null,
link								text		not null,
piece							int,
room							int,
surface						decimal(5, 2),
price							decimal(5, 2),
currency						varchar(5),
price_updated_date	datetime,
city								varchar(50),
agency_tel					varchar(30),
agency_link					text,
available						bit,
creation_date				datetime,
source							varchar(30),
type								int
)