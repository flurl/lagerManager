#V1120

DROP PROCEDURE IF EXISTS sp_getPeriodStartEnd;
DELIMITER //
CREATE PROCEDURE sp_getPeriodStartEnd( 
                    IN periodId int unsigned,
                    OUT pStart datetime,
                    OUT pEnd datetime)
BEGIN
    select 
    periode_start, periode_ende INTO pStart, pEnd
    from perioden 
    where periode_id = periodId;
    
END //
DELIMITER ;