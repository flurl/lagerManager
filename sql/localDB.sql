create table perioden(
	periode_id integer auto_increment primary key not null,
	periode_bezeichnung varchar(255) not null,
	periode_checkpoint_jahr int null,
	periode_start datetime not null,
	periode_ende datetime not null
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
	foreign key journal_checkpoints_periode_fk (checkpoint_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE tische_aktiv(
    tisch_id int NOT NULL,
    tisch_bereich int NOT NULL,
    tisch_pri_nummer int NOT NULL,
    tisch_sek_nummer int NOT NULL,
    tisch_gast int NULL,
    tisch_dt_erstellung datetime NOT NULL,
    tisch_dt_aktivitaet datetime NOT NULL,
    tisch_kellner int NOT NULL,
    tisch_fertig bit NOT NULL,
    tisch_zahlungsart int NULL,
    tisch_rechnung int NULL,
    tisch_dt_zusatz datetime NULL,
    tisch_adresse int NULL,
    tisch_kellner_abrechnung int NULL,
    tisch_client varchar(50) NULL,
    tisch_reservierung int NULL,
    tisch_reservierung_check bit NOT NULL,
    tisch_zusatz_text text NULL,
    checkpoint_tag int NULL,
    checkpoint_monat int NULL,
    checkpoint_jahr int NULL,
    tisch_externer_beleg bit NOT NULL,
    tisch_periode int not null,
    index tische_aktiv_idx (tisch_id),
    foreign key tische_aktiv_periode_fk (tisch_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE tische_bons(
    tisch_bon_id int NOT NULL,
    tisch_bon_dt_erstellung datetime NOT NULL,
    tisch_bon_tisch int NOT NULL,
    tisch_bon_kellner int NOT NULL,
    tisch_bon_client varchar(50) NOT NULL,
    tisch_bon_typ int NOT NULL,
    tisch_bon_bestellkarte int NULL,
    tisch_bon_vorgangsart int NULL,
    tisch_bon_periode int not null,
    index tische_bons_idx (tisch_bon_id),
    foreign key tische_bons_periode_fk (tisch_bon_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE tische_bondetails(
    tisch_bondetail_id int NOT NULL,
    tisch_bondetail_bon int NOT NULL,
    tisch_bondetail_master_id int NULL,
    tisch_bondetail_menge int NOT NULL,
    tisch_bondetail_absmenge int NOT NULL,
    tisch_bondetail_istUmsatz bit NOT NULL,
    tisch_bondetail_artikel int NOT NULL,
    tisch_bondetail_preis decimal(18, 3) NOT NULL,
    tisch_bondetail_text varchar(50) NOT NULL,
    tisch_bondetail_mwst int NOT NULL,
    tisch_bondetail_gangfolge int NOT NULL,
    tisch_bondetail_hatRabatt bit NOT NULL,
    tisch_bondetail_istRabatt bit NOT NULL,
    tisch_bondetail_autoEintrag bit NOT NULL,
    tisch_bondetail_stornoFaehig bit NOT NULL,
    tisch_bondetail_ep decimal(18, 2) NULL,
    tisch_bondetail_ep_mwst int NULL,
    tisch_bondetail_preisgruppe int NULL,
    tisch_bondetail_gutschein_log int NULL,
    journal_preisgruppe varchar(50) NULL,
    journal_gruppe varchar(2000) NULL,
    journal_mwst decimal(18, 3) NULL,
    tisch_bondetail_istExternerBeleg bit NOT NULL,
    tisch_bondetail_periode int not null,
    index tische_bondetails_idx (tisch_bondetail_id),
    foreign key tische_bondetails_periode_fk (tisch_bondetail_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE tische_bereiche(
    tischbereich_id int NOT NULL,
    tischbereich_kurzName varchar(8) NOT NULL,
    tischbereich_name varchar(50) NOT NULL,
    tischbereich_istGastBereich bit NOT NULL,
    tischbereich_minNummer int NOT NULL,
    tischbereich_maxNummer int NOT NULL,
    tischbereich_istAufwand bit NOT NULL,
    tischbereich_istSammelbereich bit NOT NULL,
    tischbereich_benoetigtAdresse bit NOT NULL,
    tischbereich_rechnungsAnzahl int NOT NULL,
    tischbereich_extern bit NOT NULL,
    tischbereich_istOrdercardBereich bit NOT NULL,
    tischbereich_vorgangsart int NULL,
    tischbereich_temp bit NOT NULL,
    tischbereich_versteckeSammeltisch bit NOT NULL,
    tischbereich_sammeltischOptional bit NOT NULL,
    tischbereich_rksv bit NOT NULL,
    tischbereich_periode int not null,
    index tische_bereiche_idx (tischbereich_id),
    foreign key tische_bereiche_periode_fk (tischbereich_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE rechnungen_basis(
    rechnung_id int NOT NULL,
    rechnung_typ int NOT NULL,
    rechnung_nr int NOT NULL,
    rechnung_dt_erstellung datetime NOT NULL,
    rechnung_kellnerKurzName varchar(50) NOT NULL,
    rechnung_tischCode varchar(50) NOT NULL,
    rechnung_tischBereich varchar(50) NOT NULL,
    rechnung_adresse int NULL,
    rechnung_istStorno bit NOT NULL,
    rechnung_retour decimal(18, 2) NULL,
    rechnung_dt_zusatz datetime NULL,
    checkpoint_tag int NULL,
    checkpoint_monat int NULL,
    checkpoint_jahr int NULL,
    rechnung_kassenidentifikation varchar(2000) NULL,
    rechnung_barumsatz_nr int NULL,
    rechnung_gesamt_umsatz decimal(18, 3) NULL,
    rechnung_zertifikat_id varchar(2000) NULL,
    rechnung_referenz int NULL,
    rechnung_signatur varchar(2000) NULL,
    rechnung_druckpfad varchar(2000) NULL,
    rechnung_mwst_normal decimal(18, 3) NULL,
    rechnung_mwst_ermaessigt1 decimal(18, 3) NULL,
    rechnung_mwst_ermaessigt2 decimal(18, 3) NULL,
    rechnung_mwst_null decimal(18, 3) NULL,
    rechnung_mwst_besonders decimal(18, 3) NULL,
    rechnung_gesamt_umsatz_enc varchar(2000) NULL,
    rechnung_rka varchar(2000) NULL,
    rechnung_vorherige_signatur varchar(2000) NULL,
    rechnung_beleg_kennzeichen varchar(2000) NULL,
    rechnung_istTrainingsBeleg bit NOT NULL,
    rechnung_periode int not null,
	index rechnungen_basis_idx (rechnung_id),
	foreign key rechnungen_basis_periode_fk (rechnung_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE rechnungen_details(
	rechnung_detail_id int NOT NULL,
	rechnung_detail_rechnung int NOT NULL,
	rechnung_detail_master_detail int NULL,
	rechnung_detail_menge int NOT NULL,
	rechnung_detail_absmenge int NOT NULL,
	rechnung_detail_text varchar(50) NOT NULL,
	rechnung_detail_mwst int NOT NULL,
	rechnung_detail_preis decimal(18, 3) NOT NULL,
	rechnung_detail_artikel_gruppe text NULL,
	rechnung_detail_text_2 text NULL,
	rechnung_detail_bonierdatum datetime NULL,
	rechnung_detail_periode int not null,
	index rechnungen_details_idx (rechnung_detail_id),
	foreign key rechnungen_details_periode_fk (rechnung_detail_periode) references perioden(periode_id)
) ENGINE=INNODB;



CREATE TABLE artikel_zutaten(
	zutate_master_artikel int NOT NULL,
    zutate_artikel int NOT NULL,
    zutate_menge float NOT NULL,
    zutate_istFixiert bit NOT NULL,
    zutate_istZutat bit NOT NULL,
    zutate_istRezept bit NOT NULL,
    zutate_immerAnzeigen bit NOT NULL,
    zutate_istZwangsAbfrage bit NOT NULL,
    zutate_preisVerwenden bit NOT NULL,
	zutate_periode int not null,
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
	artikel_rksv bit NOT NULL,
	artikel_externer_beleg bit NOT NULL,
	artikel_periode int null,
	index (artikel_id),
	foreign key artikel_basis_periode_fk (artikel_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE artikel_gruppen(
	artikel_gruppe_id int NOT NULL,
	artikel_gruppe_parent_id int NULL,
	artikel_gruppe_name varchar(50) NOT NULL,
	artikel_gruppe_standard_gangfolge int NOT NULL,
	artikel_gruppe_bontyp int NULL,
	artikel_gruppe_istUmsatz bit NOT NULL,
	artikel_gruppe_zeigeAufRechnung bit NOT NULL,
	artikel_gruppe_druckeRezeptur bit NOT NULL,
	artikel_gruppe_keinStorno bit NOT NULL,
	artikel_gruppe_periode int not null,
	index (artikel_gruppe_id),
	foreign key artikel_gruppe_periode_fk (artikel_gruppe_periode) references perioden(periode_id)
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
) ENGINE=INNODB;


CREATE TABLE meta_mwstgruppen (
	mwst_id int NOT NULL,
	mwst_satz decimal(18, 2) NOT NULL,
	mwst_bezeichnung varchar(50) NOT NULL,
	mwst_satz_normal bit NOT NULL,
	mwst_satz_ermaessigt_1 bit NOT NULL,
	mwst_satz_ermaessigt_2 bit NOT NULL,
	mwst_satz_null bit NOT NULL,
	mwst_satz_besonders bit NOT NULL,
	mwst_periode integer not null,
	foreign key mwst_periode_fk (mwst_periode) references perioden(periode_id)
) ENGINE=INNODB;


CREATE TABLE kellner_basis(
	kellner_id int NOT NULL,
	kellner_kurzName varchar(50) NOT NULL,
	kellner_uid int NOT NULL,
	kellner_person int NOT NULL,
	kellner_lager int NULL,
	kellner_schnellTisch_bereich int NULL,
	kellner_schnellTisch_pri_nummer int NULL,
	kellner_schnellTisch_sek_nummer int NULL,
	kellner_zeigeAuswahl bit NOT NULL,
	kellner_kasse int NULL,
	kellner_periode int not null,
	index (kellner_id),
	foreign key kellner_basis_periode_fk (kellner_periode) references perioden(periode_id)
) ENGINE=INNODB;




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



create table lieferanten(
	lieferant_id integer auto_increment primary key not null,
	lieferant_name varchar(255) not null,
	lft_ist_verbraucher tinyint(1) not null default 0
) ENGINE=INNODB;

create table lieferungen(
	lieferung_id integer unsigned auto_increment primary key not null,
	lieferant_id int not null,
	datum datetime not null,
	lie_ist_verbrauch tinyint(1) not null default 0,
	lie_kommentar MEDIUMTEXT null,
	lie_summe float not null,
	foreign key lieferung_lieferant_fk (lieferant_id) references lieferanten(lieferant_id)
) ENGINE=INNODB;


create table steuersaetze (
	sts_id int unsigned auto_increment primary key not null,
	sts_bezeichnung varchar(255) not null,
	sts_prozent float not null
) ENGINE=INNODB;


create table lieferungen_details(
	lieferung_detail_id integer auto_increment primary key not null,
	lieferung_id int unsigned not null,
	artikel_id int not null,
	anzahl float not null,
	einkaufspreis float not null,
	lde_stsid int unsigned null,
	foreign key lieferung_detail_lieferung_fk (lieferung_id) references lieferungen(lieferung_id),
	foreign key lieferung_detail_steuersatz_fk (lde_stsid) references steuersaetze(sts_id)
) ENGINE=INNODB;


create table dokumente (
	dok_id integer unsigned auto_increment primary key not null,
	dok_dotid int unsigned not null,
	dok_bezeichnung varchar(255) not null,
	dok_ocr MEDIUMTEXT null,
	dok_data longblob not null,
	dok_datum datetime not null,
	dok_lieferung_id integer unsigned null,
	foreign key dokumente_dokumenttyp_fk (dok_dotid) references dokumenttypen(dot_id),
	foreign key dokumente_lieferung_fk (dok_lieferung_id) references lieferungen(lieferung_id)
) ENGINE=INNODB;



create table liefereinheiten (
	lei_id int unsigned auto_increment primary key not null,
	lei_bezeichnung varchar(255) not null,
	lei_menge float not null
) ENGINE=INNODB;


create table bilder (
	bil_id int unsigned auto_increment primary key not null,
	bil_ocr MEDIUMTEXT null,
	bil_data longblob not null,
	bil_dokid integer unsigned not null,
	foreign key bilder_dokument_fk (bil_dokid) references dokumente(dok_id)
) ENGINE=INNODB;


create table beschaeftigungsbereiche (
	beb_id int unsigned auto_increment primary key not null,
	beb_bezeichnung varchar(255) not null,
	beb_trinkgeldpauschale bool not null default 0
) ENGINE=INNODB;


create table dienstnehmer (
	din_id int unsigned auto_increment primary key not null,
	din_name varchar(255) not null,
	din_nummer varchar(255) not null,
	din_gehalt decimal(18, 3) NOT NULL,
	din_gehid int unsigned not null,
	din_bebid int unsigned not null,
	din_stundensatz decimal(18, 3) NOT NULL,
	din_farbe varchar(255) NULL,
	din_svnr varchar(255) NULL,
	foreign key dienstnehmer_beschaeftigunsgbereich_fk (din_bebid) references beschaeftigungsbereiche(beb_id),
	foreign key dienstnehmer_gehalt_fk (din_gehid) references gehaelter (geh_id),
	unique key (din_nummer)
) ENGINE=INNODB;


create table veranstaltungen (
	ver_id int unsigned auto_increment primary key not null,
	ver_datum date not null,
	ver_bezeichnung varchar(255) not null,
	ver_beginn time not null,
	ver_checkpointid int null,
	foreign key veranstaltung_checkpoint_fk (ver_checkpointid) references journal_checkpoints(checkpoint_id)
) ENGINE=INNODB;
	
	
create table arbeitsplaetze (
	arp_id int unsigned auto_increment primary key not null,
	arp_bezeichnung varchar(255) not null,
	arp_std_dienst_dauer float not null,
	arp_bebid int unsigned not null,
	foreign key arbeitsplatz_beschaeftigungsbereich_fk (arp_bebid) references beschaeftigungsbereiche(beb_id)
) ENGINE=INNODB;

create table dienste (
	die_id int unsigned auto_increment primary key not null,
	die_dinid int unsigned not null,
	die_verid int unsigned not null,
	die_arpid int unsigned not null,
	die_beginn datetime not null,
	die_ende datetime not null,
	die_pause float not null,
	foreign key dienst_dienstnehmer_fk (die_dinid) references dienstnehmer(din_id),
	foreign key dienst_veranstaltung_fk (die_verid) references veranstaltungen(ver_id),
	foreign key dienst_arbeitsplatz_fk (die_arpid) references arbeitsplaetze(arp_id)
) ENGINE=INNODB;


create table dienste_vorlagen (
	div_id int unsigned auto_increment primary key not null,
	div_bezeichnung varchar(255) not null,
	div_arpid int unsigned not null,
	div_beginn time not null,
	div_ende time not null,
	foreign key dienstvorlage_arbeitsplatz_fk (div_arpid) references arbeitsplaetze(arp_id)
) ENGINE=INNODB;


create table buchungskonten (
	buk_id int unsigned auto_increment primary key not null,
	buk_nummer varchar(255) not null,
	buk_bezeichnung varchar(255) not null
) ENGINE=INNODB;


create table buchungskonto2artikel (
	b2a_id int unsigned auto_increment primary key not null,
	b2a_bukid int unsigned not null,
	b2a_artikel_id int not null,
	b2a_periode int not null,
	foreign key b2a_buchungskonto_fk (b2a_bukid) references buchungskonten(buk_id),
	foreign key b2a_artikel_fk (b2a_artikel_id) references artikel_basis(artikel_id),
	foreign key b2a_periode_fk (b2a_periode) references perioden(periode_id),
	unique key (b2a_bukid, b2a_artikel_id, b2a_periode)
) ENGINE=INNODB;


create table config (
	cfg_id int unsigned auto_increment primary key not null,
	cfg_key varchar(255) not null,
	cfg_valueI int null,
	cfg_valueF float null,
	cfg_valueS text null,
	unique key (cfg_key)
) ENGINE=INNODB;


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



--20120927
insert into dokumenttypen (dot_bezeichnung) values ('Eingangsrechnung');

--20131706
alter table journal_checkpoints ENGINE=INNODB;


--20130719
--this update has to be made on the wiffzack database
/*update artikel_basis
set artikel_ep = 
(select (artikel_preise_preis/3)/(1+mwst_satz/100) from artikel_preise, meta_preisgruppen, meta_mwstgruppen
where artikel_preise_artikel_id = artikel_id 
and  artikel_preise_preisgruppe_id = preisgruppe_id 
and preisgruppe_name = 'Normalpreis'
and artikel_preise_mwst = mwst_id),
artikel_ep_mwst = 
(select artikel_preise_mwst from artikel_preise, meta_preisgruppen 
where artikel_preise_artikel_id = artikel_id 
and  artikel_preise_preisgruppe_id = preisgruppe_id 
and preisgruppe_name = 'Normalpreis')*/



--20130901
--insert into config (cfg_key, cfg_valueI) values ('considerNAZ', 1);

--20150224
--insert into config (cfg_key, cfg_valueF) values ('trinkgeldpauschale', 0.2725);
--insert into config (cfg_key, cfg_valueF) values ('nachtarbeitszuschlag', 20.7);
