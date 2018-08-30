#V1203


alter table dienstnehmer add column din_vorname varchar(255) not null;

update dienstnehmer
set din_vorname = substring(din_name, 1, locate(" ", din_name)),
din_name = substring(din_name, locate(" ", din_name));

alter table dienstnehmer change din_name din_nachname varchar(255) not null
