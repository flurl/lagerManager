#V1142
#V1139
#V0110


create table initialer_stand (
	ist_id integer auto_increment primary key not null,
	ist_artikel_id int not null,
	ist_anzahl float not null,
	ist_arp_id int unsigned not null,
	ist_periode_id int not null,
	foreign key initialer_stand_artikel_fk (ist_artikel_id) references artikel_basis(artikel_id),
	foreign key initialer_stand_periode_fk (ist_periode_id) references perioden(periode_id),
	foreign key initialer_stand_arbeitsplatz_fk (ist_arp_id) references arbeitsplaetze(arp_id)
) ENGINE=INNODB;

