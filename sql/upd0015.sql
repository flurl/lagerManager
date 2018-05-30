#V1193


create table feiertage (
    fta_id int unsigned auto_increment primary key not null,
    fta_datum datetime unique not null,
    fta_bezeichnung varchar(255) not null
) ENGINE=INNODB;

