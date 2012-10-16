create table perioden(
	periode_id integer auto_increment primary key not null,
	periode_bezeichnung varchar(255) not null,
	periode_checkpoint_jahr int null,
	periode_start datetime not null,
	periode_ende datetime not null
) ENGINE=INNODB;

CREATE TABLE journal_details(
	detail_id int NOT NULL,
	detail_journal int NOT NULL,
	detail_absmenge int NOT NULL,
	detail_istUmsatz bit NOT NULL,
	detail_preis decimal(18, 3) NOT NULL,
	detail_artikel_text varchar(50) NOT NULL,
	detail_mwst decimal(18, 2) NOT NULL,
	detail_bonier_datum datetime NOT NULL,
	detail_gruppe varchar(255) NOT NULL,
	detail_istRabatt bit NOT NULL,
	detail_rabatt int NULL,
	detail_kellner varchar(50) NULL,
	detail_autoEintrag bit NOT NULL,
	detail_ep decimal(18, 3) NULL,
	detail_ep_mwst decimal(18, 2) NULL,
	detail_bestellkarte int NULL,
	detail_client varchar(50) NULL,
	detail_preisgruppe varchar(50) NULL,
	detail_vorgangsart int NULL,
	detail_gutschein_log int NULL,
	detail_periode int null,
	index journal_details_artikel_text_idx (detail_artikel_text),
	index journal_details_journal_idx (detail_journal),
	foreign key journal_details_periode_fk (detail_periode) references perioden(periode_id)
) ENGINE=INNODB;

CREATE TABLE journal_daten(
	daten_rechnung_id int NOT NULL,
	daten_checkpoint_tag int NOT NULL,
	daten_checkpoint_monat int NULL,
	daten_checkpoint_jahr int NULL,
	daten_checkpoint_kellner int NULL,
	daten_periode int null,
	index journal_daten_rechnung_idx (daten_rechnung_id),
	index journal_daten_tag_idx (daten_checkpoint_tag),
	foreign key journal_daten_periode_fk (daten_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE journal_checkpoints(
	checkpoint_id int NOT NULL,
	checkpoint_typ varchar(10) NOT NULL,
	checkpoint_datum datetime NOT NULL,
	checkpoint_anmerkung text NULL,
	checkpoint_info text NOT NULL,
	checkpoint_num int NOT NULL,
	checkpoint_kassenbuch_verarbeitet bit NOT NULL,
	checkpoint_periode int not null,
	index journal_checkpoints_idx (checkpoint_id),
	index journal_checkpoints_periode_idx (checkpoint_periode),
	foreign key journal_checkpoints_periode_fk (checkpoint_periode) references perioden(periode_id)
);


CREATE TABLE artikel_zutaten(
	zutate_master_artikel int NOT NULL,
	zutate_artikel int NOT NULL,
	zutate_menge float NOT NULL,
	zutate_istFixiert int NOT NULL,
	zutate_istZutat int NOT NULL,
	zutate_istRezept int NOT NULL,
	zutate_immerAnzeigen int NOT NULL,
	zutate_istZwangsAbfrage int NOT NULL,
	zutate_preisVerwenden int NOT NULL,
	zutate_periode int null,
	index (zutate_master_artikel),
	index (zutate_artikel),
	foreign key artikel_zutaten_periode_fk (zutate_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE artikel_basis(
	artikel_id int NOT NULL,
	artikel_bezeichnung varchar(50) NOT NULL,
	artikel_gruppe int NOT NULL,
	artikel_ep decimal(18, 2) NULL,
	artikel_ep_mwst int NULL,
	artikel_preis_popup bit NOT NULL,
	artikel_ep_preis_popup bit NOT NULL,
	artikel_bemerkung text NULL,
	artikel_bezeichnung_2 text NULL,
	artikel_periode int null,
	index (artikel_id),
	foreign key artikel_basis_periode_fk (artikel_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE lager_artikel(
	lager_artikel_lagerartikel int NOT NULL,
	lager_artikel_lieferant int NOT NULL,
	lager_artikel_lieferant_artikel varchar(20) NULL,
	lager_artikel_artikel int NOT NULL,
	lager_artikel_prioritaet int NOT NULL,
	lager_artikel_einheit int NULL,
	lager_artikel_lager int NULL,
	lager_artikel_flags int NOT NULL,
	lager_artikel_maxStand float NOT NULL,
	lager_artikel_minStand float NOT NULL,
	lager_artikel_periode int null,
	index (lager_artikel_lagerartikel),
	index (lager_artikel_artikel),
	foreign key lager_artikel_periode_fk (lager_artikel_periode) references perioden(periode_id)
) ENGINE=INNODB;


create table lager_einheiten(
	lager_einheit_id int NOT NULL,
	lager_einheit_name text not null,
	lager_einheit_multiplizierer float not null,
	lager_einheit_basis int null,
	lager_einheit_periode int not null,
	index (lager_einheit_id),
	foreign key lager_einheit_periode_fk (lager_einheit_periode) references perioden(periode_id)
);




create table lagerstand(
	lagerstand_id integer auto_increment primary key not null,
	artikel_id int not null,
	anzahl float not null,
	periode_id int null,
	foreign key lagerstand_artikel_fk (artikel_id) references artikel_basis(artikel_id),
	foreign key lagerstand_periode_fk (periode_id) references perioden(periode_id)
) ENGINE=INNODB;


create table dokumenttypen (
	dot_id integer unsigned auto_increment primary key not null,
	dot_bezeichnung varchar(255) not null
) ENGINE=INNODB;


create table dokumente (
	dok_id integer unsigned auto_increment primary key not null,
	dok_dotid int unsigned not null,
	dok_bezeichnung varchar(255) not null,
	dok_ocr MEDIUMTEXT null,
	dok_data longblob not null,
	dok_datum datetime not null,
	foreign key dokumente_dokumenttyp_fk (dok_dotid) references dokumenttypen(dot_id)
) ENGINE=INNODB;


create table lieferanten(
	lieferant_id integer auto_increment primary key not null,
	lieferant_name varchar(255) not null
) ENGINE=INNODB;

create table lieferungen(
	lieferung_id integer auto_increment primary key not null,
	lieferant_id int not null,
	datum datetime not null,
	lie_dokid int unsigned null,
	foreign key lieferung_lieferant_fk (lieferant_id) references lieferanten(lieferant_id),
	foreign key lieferung_dokument_fk (lie_dokid) references dokumente(dok_id)
) ENGINE=INNODB;

create table lieferungen_details(
	lieferung_detail_id integer auto_increment primary key not null,
	lieferung_id int not null,
	artikel_id int not null,
	anzahl float not null,
	einkaufspreis float not null,
	foreign key lieferung_detail_lieferung_fk (lieferung_id) references lieferungen(lieferung_id)
) ENGINE=INNODB;


create table steuersaetze (
	sts_id int unsigned auto_increment primary key not null,
	sts_bezeichnung varchar(255) not null,
	sts_prozent float not null
) ENGINE=INNODB;






alter table journal_details add index journal_details_artikel_text_idx (detail_artikel_text);
alter table journal_details add index journal_details_journal_idx (detail_journal);
alter table journal_daten add index journal_daten_rechnung_idx (daten_rechnung_id);
alter table journal_daten add index journal_daten_tag_idx (daten_checkpoint_tag);
alter table journal_checkpoints add index journal_checkpoints_id_idx (checkpoint_id);


--20120831
alter table journal_details add column detail_periode int null;
alter table journal_details add foreign key journal_details_periode_fk (detail_periode) references perioden(periode_id);
update journal_details set detail_periode = 1;

alter table journal_daten add column daten_periode int null;
alter table journal_daten add foreign key journal_daten_periode_fk (daten_periode) references perioden(periode_id);
update journal_daten set daten_periode = 1;

alter table journal_checkpoints add column checkpoint_periode int null;
alter table journal_checkpoints add foreign key journal_checkpoints_periode_fk (checkpoint_periode) references perioden(periode_id);
update journal_checkpoints set checkpoint_periode = 1;



--20120927
alter table lieferungen add column lie_dokid int unsigned null;
alter table lieferungen add foreign key lieferung_dokument_fk (lie_dokid) references dokumente(dok_id);
insert into dokumenttypen (dot_bezeichnung) values ('Eingangsrechnung');


--20120928
alter table dokumente add dok_datum datetime not null;
alter table dokumente modify dok_data longblob not null;

--20121006
alter table dokumente modify dok_ocr MEDIUMTEXT null;

--20121016
alter table lieferungen_details drop foreign key lieferungen_details_ibfk_2;

