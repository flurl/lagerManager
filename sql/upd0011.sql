#V1156


call AddColumnUnlessExists(Database(), 'tische_aktiv', 'tisch_externer_beleg', 'bit NOT NULL');

call AddColumnUnlessExists(Database(), 'tische_bondetails', 'tisch_bondetail_istExternerBeleg', 'bit NOT NULL');

call AddColumnUnlessExists(Database(), 'tische_bereiche', 'tischbereich_rksv', 'bit NOT NULL');

call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_kassenidentifikation', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_barumsatz_nr', 'int NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_gesamt_umsatz' ,'decimal(18, 3) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_zertifikat_id', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_referenz', 'int NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_signatur', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_druckpfad', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_mwst_normal', 'decimal(18, 3) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_mwst_ermaessigt1', 'decimal(18, 3) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_mwst_ermaessigt2', 'decimal(18, 3) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_mwst_null', 'decimal(18, 3) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_mwst_besonders', 'decimal(18, 3) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_gesamt_umsatz_enc', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_rka', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_vorherige_signatur', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_beleg_kennzeichen', 'varchar(2000) NULL');
call AddColumnUnlessExists(Database(), 'rechnungen_basis', 'rechnung_istTrainingsBeleg', 'bit NOT NULL');

call AddColumnUnlessExists(Database(), 'artikel_basis', 'artikel_rksv', 'bit NOT NULL');

