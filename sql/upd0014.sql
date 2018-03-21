#V1177


create table gezaehlter_stand (
	gst_id integer auto_increment primary key not null,
	gst_datum datetime not null,
	gst_artikel_id int not null,
	gst_anzahl float not null,
	foreign key initialer_stand_artikel_fk (gst_artikel_id) references artikel_basis(artikel_id),
	index gezaehlter_stand_datum_idx (gst_datum)
) ENGINE=INNODB;

