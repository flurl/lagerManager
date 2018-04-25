#V1121

DROP FUNCTION IF EXISTS getPurchasePrice;
DELIMITER //
CREATE FUNCTION getPurchasePrice(
                    artikelBez varchar(255), 
                    periodId int unsigned,
                    maxDate datetime)
returns float
BEGIN
    declare ek float default 0.0;
    declare totalEk float default 0.0;
    declare pStart datetime;
    declare pEnd datetime;
    declare artikelId integer;
    declare anzahlLagerArtikel integer;
    declare bezeichnung varchar(255) default "";
    declare mengenFaktor float;
    declare finished integer default 0;
    
    select artikel_id into artikelId from artikel_basis where artikel_bezeichnung = artikelBez  and artikel_periode = periodId;
    
    select count(*) into anzahlLagerArtikel from lager_artikel where lager_artikel_artikel = artikelId and lager_artikel_periode = periodId;
    
    /* not a lager_artikel, so it must be a receipe */
    if anzahlLagerArtikel = 0 then
        CREATE TEMPORARY TABLE IF NOT EXISTS temp_artikel ENGINE=MEMORY as (
        select art2.artikel_id as aId, zutate_menge/lager_einheit_multiplizierer as faktor
        from (artikel_basis as art1, artikel_basis as art2, artikel_zutaten)
        left outer join lager_artikel on lager_artikel_artikel = art2.artikel_id
        left outer join lager_einheiten on lager_artikel_einheit = lager_einheit_id
        where 1=1
        and art1.artikel_id = artikelId
        and zutate_master_artikel = art1.artikel_id
        and zutate_artikel = art2.artikel_id
        and zutate_istRezept = 1
        and art1.artikel_periode = periodId
        and art2.artikel_periode = periodId
        and zutate_periode = periodId
        and (lager_artikel_periode = periodId or lager_artikel_periode is null)
        and (lager_einheit_periode = periodId or lager_einheit_periode is null)
        );
        
    else
        CREATE TEMPORARY TABLE IF NOT EXISTS temp_artikel ENGINE=MEMORY as (
        select artikelId as aId, 1.0 as faktor
        );
        
    end if;
    
    call sp_getPeriodStartEnd(periodId, pStart, pEnd);
    
    BEGIN
    declare artikel_cursor cursor for 
    select * from temp_artikel;
    
    DECLARE CONTINUE HANDLER 
    FOR NOT FOUND SET finished = 1;
    
    open artikel_cursor;
    
    fetch_artikel: loop
    
        fetch artikel_cursor into artikelId, mengenFaktor;
        
        if finished = 1 then
            leave fetch_artikel;
        end if;
        
        select (sum(anzahl*einkaufspreis)/sum(anzahl))*mengenFaktor into ek
        from artikel_basis, lieferungen_details, lieferungen
        where 1=1 
        and anzahl > 0 /* don't count verbräuche */
        and lieferungen_details.lieferung_id = lieferungen.lieferung_id
        and lieferungen_details.artikel_id = artikel_basis.artikel_id  
        and lieferungen.datum between pStart and pEnd
        and artikel_basis.artikel_periode = periodId
        and (lieferungen.datum <= maxDate or maxDate is null)
        and artikel_basis.artikel_id = artikelId;
        
        set totalEk = totalEk + ek;
    
    end loop fetch_artikel;
    
    close artikel_cursor;
    
    drop temporary table if exists temp_artikel;
    
    return(totalEk);
    END;
    
END //
DELIMITER ;
