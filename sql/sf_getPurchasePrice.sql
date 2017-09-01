#V1121

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
    
    select sum(anzahl*einkaufspreis)/sum(anzahl) into ek
                from artikel_basis, lieferungen_details, lieferungen
                where 1=1 
                and anzahl > 0 /* don't count verbräuche */
                and lieferungen_details.lieferung_id = lieferungen.lieferung_id
                and lieferungen_details.artikel_id = artikel_basis.artikel_id  
                and lieferungen.datum between pStart and pEnd
                and artikel_basis.artikel_periode = periodId
                and (lieferungen.datum <= maxDate or maxDate is null)
                and artikel_bezeichnung = artikelBez;
    
    return(ek);
    
END //
DELIMITER ;
