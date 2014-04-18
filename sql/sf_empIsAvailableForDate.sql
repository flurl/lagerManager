#V1081
DROP FUNCTION IF EXISTS empIsAvailableForDate;
DELIMITER //
CREATE FUNCTION empIsAvailableForDate(
                    empId int unsigned, 
                    dat date)
returns int unsigned
BEGIN
    declare isAvailable int unsigned;
    
    select count(*)
    into isAvailable
    from dienstnehmer as din_out, dienstnehmer_ereignisse as dir_out, dir_typen as dit_out 
    where 1=1
    and din_id = dir_dinid
    and dir_ditid = dit_id
    and dit_kbez = 'EIN'
    and dir_out.dir_datum > (select ifnull(max(dir_in.dir_datum), '1900-01-01')
        from dir_typen as dit_in, dienstnehmer_ereignisse as dir_in 
        where 1=1 
        and dit_in.dit_kbez = 'AUS' 
        and dir_in.dir_ditid = dit_in.dit_id
        and dir_in.dir_dinid = din_out.din_id
        and dir_in.dir_datum <= dat)
    and din_out.din_id = empId
    and dir_out.dir_datum <= dat;
    
    return(isAvailable);
    
END //
DELIMITER ;