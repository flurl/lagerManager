#V1156

alter table tische_aktiv add column tisch_externer_beleg bit NOT NULL;

alter table tische_bondetails add column tisch_bondetail_istExternerBeleg bit NOT NULL;

alter table tische_bereiche add column tischbereich_rksv bit NOT NULL;

alter table rechnungen_basis add column rechnung_kassenidentifikation varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_barumsatz_nr int NULL;
alter table rechnungen_basis add column rechnung_gesamt_umsatz decimal(18; 3) NULL;
alter table rechnungen_basis add column rechnung_zertifikat_id varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_referenz int NULL;
alter table rechnungen_basis add column rechnung_signatur varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_druckpfad varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_mwst_normal decimal(18; 3) NULL;
alter table rechnungen_basis add column rechnung_mwst_ermaessigt1 decimal(18; 3) NULL;
alter table rechnungen_basis add column rechnung_mwst_ermaessigt2 decimal(18; 3) NULL;
alter table rechnungen_basis add column rechnung_mwst_null decimal(18; 3) NULL;
alter table rechnungen_basis add column rechnung_mwst_besonders decimal(18; 3) NULL;
alter table rechnungen_basis add column rechnung_gesamt_umsatz_enc varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_rka varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_vorherige_signatur varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_beleg_kennzeichen varchar(2000) NULL;
alter table rechnungen_basis add column rechnung_istTrainingsBeleg bit NOT NULL;

alter table artikel_basis add column artikel_rksv bit NOT NULL;
