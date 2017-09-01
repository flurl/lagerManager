#V1170


create table ek_modifikatoren (
    emo_id int unsigned auto_increment primary key not null,
    emo_artikel_id int not null,
    emo_operator enum('+', '-', '*', '/') not null,
    emo_modifikator float not null,
    emo_periode_id int not null,
    foreign key ek_modifikatoren_artikel_fk (emo_artikel_id) references artikel_basis(artikel_id),
    foreign key ek_modifikatoren_periode_fk (emo_periode_id) references perioden(periode_id)
) ENGINE=INNODB;


DROP FUNCTION IF EXISTS getPurchasePrice;
DELIMITER //
CREATE FUNCTION getPurchasePrice(
                    artikelBez varchar(255), 
                    periodId int unsigned,
                    maxDate datetime)
returns float
BEGIN
    declare ek float;
    declare pStart datetime;
    declare pEnd datetime;
    
    
    call sp_getPeriodStartEnd(periodId, pStart, pEnd);
    
    select (
        sum(anzahl*einkaufspreis)
        /sum(
            ifnull((if (emo_operator = '/', emo_modifikator, 1.0)),1.0)
        )
        *sum(
            ifnull((if (emo_operator = '*', emo_modifikator, 1.0)),1.0)
        )
        +sum(
            ifnull((if (emo_operator = '+', emo_modifikator, 0.0)),0.0)
        )
        -sum(
            ifnull((if (emo_operator = '-', emo_modifikator, 0.0)),0.0)
        )
    )
    /sum(anzahl) into ek
    from lieferungen_details, lieferungen,
        artikel_basis left outer join ek_modifikatoren on emo_artikel_id = artikel_basis.artikel_id
    where 1=1 
    and anzahl > 0 /* don't count verbräuche */
    and lieferungen_details.lieferung_id = lieferungen.lieferung_id
    and lieferungen_details.artikel_id = artikel_basis.artikel_id  
    and lieferungen.datum between pStart and pEnd
    and artikel_basis.artikel_periode = periodId
    and (emo_periode_id = periodId or emo_periode_id is null)
    and (lieferungen.datum <= maxDate or maxDate is null)
    and artikel_bezeichnung = artikelBez;
    
    return(ek);
    
END //
DELIMITER ;

