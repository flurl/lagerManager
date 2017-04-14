#V1146

CREATE TABLE IF NOT EXISTS tische_bereiche(
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
    tischbereich_periode int not null,
    index tische_bereiche_idx (tischbereich_id),
    foreign key tische_bereiche_periode_fk (tischbereich_periode) references perioden(periode_id)
) ENGINE=INNODB;

